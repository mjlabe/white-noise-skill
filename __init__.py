from multiprocessing import Process
from os.path import join, abspath, dirname, isfile

from mycroft import intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.skills.context import *
from mycroft.skills.core import MycroftSkill
from mycroft.util import play_mp3
from mycroft.util.parse import extract_number


class WhiteNoise(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # Register list of white noise titles that are held in a padatious entity
        self.process = None
        self.kill_process = None
        self.audio_file = self.settings.get('audio_file_path',
                                            join(abspath(dirname(__file__)), 'audio_files', 'fan.mp3'))

    @intent_file_handler('noise.white.intent')
    def handle_noise_white(self, message):
        wait_while_speaking()
        self.speak_dialog('noise.white')
        wait_while_speaking()

        secs = None
        if message.data['duration']:
            duration = message.data["duration"]
            secs = self._extract_duration(duration)
        if isfile(self.audio_file):
            self.process = play_mp3(self.audio_file)
        else:
            self.speak_dialog("Audio file not found. Using default.")
            self.process = play_mp3(self.audio_file)

        if secs:
            self.kill = Process(target=self.kill_noise, args=(secs,))
        self.kill.start()

    def kill_noise(self, time):
        time.sleep(time)
        self.log.info('killing')
        self.process.terminate()
        self.process.wait()

    def _extract_duration(self, text):
        unit = 1

        if not text:
            return None
        num = extract_number(text, self.lang)

        if not num:
            return None

        if 'sec' in text:
            unit = 1
        elif 'min' in text:
            unit = 60
        elif 'hour' in text:
            unit = 360

        return num * unit

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()


def create_skill():
    return WhiteNoise()
