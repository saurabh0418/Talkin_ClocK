import os
import pyaudio
import wave
import datetime


class TalkingClock(object):

    number_to_word = {
        0: " twelve",
        1: " one",
        2: " two",
        3: " three",
        4: " four",
        5: " five",
        6: " six",
        7: " seven",
        8: " eight",
        9: " nine",
        10: " ten",
        11: " eleven",
        12: " twelve",
        13: " thirteen",
        14: " fourteen",
        15: " fifteen",
        16: " sixteen",
        17: " seventeen",
        18: " eighteen",
        19: " nineteen",
        20: " twenty",
        30: " thirty",
        40: " fourty",
        50: " fifty",
    }

    tens_to_word = {
        2: " twenty",
        3: " thirty",
        4: " fourty",
        5: " fifty",
    }

    def time_string_to_words(self, time):
        """
        Time String to Words
        --------------------
        Convert time string in format HH:MM to its english
        speaking equivalent
        """
        try:
            hour, minutes = [int(x) for x in time.split(":")]
        except ValueError:
            raise ValueError("Time not in format 'HH:MM'")

        output = "It's"
        output += self.number_to_word[hour % 12]

        period = " am" if (hour % 24 < 12) else " pm"
        minutes = minutes % 60

        if minutes == 0:
            pass
        elif minutes < 20:
            output += (" oh" if minutes < 10 else "") + self.number_to_word[minutes]
        else:
            tens, ones = divmod(minutes, 10)
            output += self.tens_to_word[tens]

            if minutes % 10:
                output += self.number_to_word[ones]

        return output + period

    def time_to_speech(self, sentance):
        """
        Time to Speech
        --------------
        If possible, queue sound files according to sentance.
        Then, say the sentance out loud (uses speakers).
        """
        # Invert: Keys become values, values become keys
        word_to_number = {v[1:]: str(k) for k, v in self.number_to_word.items()}

        directory = os.path.dirname(os.path.realpath(__file__))

        sentance = sentance.split()

        sounds_to_play = ["HOUR1", "its"]
        am_or_pm = sentance[-1]
        above_12 = False

        sounds_to_play.append(word_to_number[sentance[1]])  # It's 'nine' thirty

        for i in ["ty", "teen"]:
            if sentance[2].endswith(i):  # It's ten ['thirty', 'thirteen', ... ]
                sounds_to_play.append(sentance[2].split(i)[0])
                sounds_to_play.append(i)
                above_12 = True

        if len(sentance) == 4 and not above_12:  # It's five ['ten', 'eleven', 'twelve']
            sounds_to_play.append(word_to_number[sentance[2]])

        if len(sentance) == 5:
            if sentance[2] == "oh":  # ex. It's nine 'oh' five am
                sounds_to_play.append("o")
            sounds_to_play.append(word_to_number[sentance[3]])  # It's nine twenty 'five' am

        sounds_to_play.append(am_or_pm)
        sounds_to_play.append("hour2")

        for i in sounds_to_play:
            self.play_sounds(os.path.join(directory, "sound_clips", i + ".wav"))

    @staticmethod
    def play_sounds(sound_path):
        chunk = 1024
        f = wave.open(sound_path, "rb")
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate = f.getframerate(),
                        output=True)

        data = f.readframes(chunk)

        while data:
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    Talker = TalkingClock()

    time = datetime.datetime.now().strftime("%H:%M")

    sentance = Talker.time_string_to_words(time)
    Talker.time_to_speech(sentance)

