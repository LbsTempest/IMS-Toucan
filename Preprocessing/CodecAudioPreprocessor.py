import dac
import torch
from dac.model import DAC
from dac.utils import load_model
from torchaudio.transforms import Resample


class AudioPreprocessor:

    def __init__(self, input_sr, output_sr=44100, device="cpu"):
        self.device = device
        self.input_sr = input_sr
        self.output_sr = output_sr
        self.resample = Resample(orig_freq=input_sr, new_freq=output_sr).to(self.device)
        self.model = DAC()
        self.model = load_model(dac.__model_version__)
        self.model.eval()
        self.model.to(device)

    def resample_audio(self, audio, current_sampling_rate):
        if current_sampling_rate != self.input_sr:
            print("warning, change in sampling rate detected. If this happens too often, consider re-ordering the audios so that the sampling rate stays constant for multiple samples")
            self.resample = Resample(orig_freq=current_sampling_rate, new_freq=self.output_sr).to(self.device)
            self.input_sr = current_sampling_rate
        audio = torch.tensor(audio, device=self.device, dtype=torch.float32)
        audio = self.resample(audio)
        return audio

    @torch.inference_mode()
    def audio_to_codec_tensor(self, audio, current_sampling_rate):
        if current_sampling_rate != self.output_sr:
            audio = self.resample_audio(audio, current_sampling_rate)
        elif type(audio) != torch.tensor:
            audio = torch.Tensor(audio)
        return self.model.encode(audio.unsqueeze(0).unsqueeze(0))["z"].squeeze()

    @torch.inference_mode()
    def audio_to_codebook_indexes(self, audio, current_sampling_rate):
        if current_sampling_rate != self.output_sr:
            audio = self.resample_audio(audio, current_sampling_rate)
        elif type(audio) != torch.tensor:
            audio = torch.Tensor(audio)
        return self.model.encode(audio.unsqueeze(0).unsqueeze(0))["codes"].squeeze()

    @torch.inference_mode()
    def indexes_to_codec_frames(self, codebook_indexes):
        if len(codebook_indexes.size()) == 2:
            codebook_indexes = codebook_indexes.unsqueeze(0)
        return self.model.quantizer.from_codes(codebook_indexes)[0].squeeze()


if __name__ == '__main__':
    import soundfile

    wav, sr = soundfile.read("../audios/speaker_references_for_testing/angry.wav")
    ap = AudioPreprocessor(input_sr=sr)

    continuous_codes = ap.audio_to_codec_tensor(wav, current_sampling_rate=sr)
    codebook_indexes = ap.audio_to_codebook_indexes(wav, current_sampling_rate=sr)
    continuous_codes_from_indexes = ap.indexes_to_codec_frames(codebook_indexes)
    print(continuous_codes_from_indexes == continuous_codes)

    import matplotlib.pyplot as plt

    plt.imshow(continuous_codes.cpu().numpy(), cmap='GnBu')
    plt.show()

    plt.imshow(continuous_codes_from_indexes.cpu().numpy(), cmap='GnBu')
    plt.show()