from pydub import AudioSegment
import io

def chunk(file_data) -> tuple[list[io.BytesIO], list[int]]:
    file_data = io.BytesIO(file_data)
    audio = AudioSegment.from_mp3(file_data)
    audio_list, len_list = [], []
    ten_minutes = 10 * 60 * 1000
    while len(audio) > 0:
        audio_segment = audio[:ten_minutes]
        audio = audio[ten_minutes:]
        buffer = io.BytesIO()
        audio_segment.export(buffer, format="mp3")
        audio_list.append(buffer)
        len_list.append(len(audio_segment))
    return audio_list, len_list
