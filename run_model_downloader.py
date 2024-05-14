import os
import urllib.request

from Utility.storage_config import MODELS_DIR


def report(block_number, read_size, total_size):
    if block_number % 1000 == 0:
        return_to_front = '\b' * 52
        percent = round(((block_number * read_size) / total_size) * 100)
        print(f"{return_to_front}[{'█' * (percent // 2)}{'.' * (50 - (percent // 2))}]", end='')
    if block_number * read_size >= total_size:
        return_to_front = '\b' * 52
        print(f"{return_to_front}Download complete!\n")


def download_models():
    #############
    print("Downloading Aligner Model")
    os.makedirs(os.path.join(MODELS_DIR, "Aligner"), exist_ok=True)
    filename, headers = urllib.request.urlretrieve(
        url="https://github.com/DigitalPhonetics/IMS-Toucan/releases/download/v2.6/aligner.pt",
        filename=os.path.abspath(os.path.join(MODELS_DIR, "Aligner", "aligner.pt")),
        reporthook=report)

    #############
    print("Downloading Multilingual ToucanTTS Model")
    os.makedirs(os.path.join(MODELS_DIR, "ToucanTTS_Meta"), exist_ok=True)
    filename, headers = urllib.request.urlretrieve(
        url="https://github.com/DigitalPhonetics/IMS-Toucan/releases/download/v2.6/ToucanTTS_Meta.pt",
        filename=os.path.abspath(os.path.join(MODELS_DIR, "ToucanTTS_Meta", "best.pt")),
        reporthook=report)

    #############
    print("Downloading Vocoder")
    os.makedirs(os.path.join(MODELS_DIR, "Vocoder"), exist_ok=True)
    filename, headers = urllib.request.urlretrieve(
        url="https://github.com/DigitalPhonetics/IMS-Toucan/releases/download/v2.6/Vocoder.pt",
        filename=os.path.abspath(os.path.join(MODELS_DIR, "Vocoder", "best.pt")),
        reporthook=report)

    #############
    print("Downloading Embedding Model")
    os.makedirs(os.path.join(MODELS_DIR, "Embedding"), exist_ok=True)
    filename, headers = urllib.request.urlretrieve(
        url="https://github.com/DigitalPhonetics/IMS-Toucan/releases/download/v2.6/embedding_function.pt",
        filename=os.path.abspath(os.path.join(MODELS_DIR, "Embedding", "embedding_function.pt")),
        reporthook=report)

    #############
    print("Downloading Embedding GAN")
    os.makedirs(os.path.join(MODELS_DIR, "Embedding"), exist_ok=True)
    filename, headers = urllib.request.urlretrieve(
        url="https://github.com/DigitalPhonetics/IMS-Toucan/releases/download/v2.6/embedding_gan.pt",
        filename=os.path.abspath(os.path.join(MODELS_DIR, "Embedding", "embedding_gan.pt")),
        reporthook=report)

    #############
    print("Downloading Codec Model")
    filename, headers = urllib.request.urlretrieve(
        url="https://huggingface.co/Dongchao/AcademiCodec/resolve/main/encodec_16k_320d.pth",
        filename=os.path.abspath(os.path.join("Preprocessing/Codec", "encodec_16k_320d.pt")),
        reporthook=report)


# TODO add asp pickle

if __name__ == '__main__':
    download_models()
