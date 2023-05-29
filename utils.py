import io
from pydub import AudioSegment


def convert_record_to_mp3(file: bytes) -> bytes:
    """
    Конвертируем файл wav в формат mp3.
    """
    audio = AudioSegment.from_file(io.BytesIO(file), format='wav')
    mp3_file = audio.export(format='mp3').read()
    return mp3_file
