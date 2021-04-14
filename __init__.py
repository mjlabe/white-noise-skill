import re
import time
from multiprocessing import Process
from os.path import join, isfile, splitext, abspath, dirname

import requests
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
        # Initialize variables and path to audio file
        # self.download_default_audio_file()
        self.process = None
        self.kill_process = None

        file_name = 'fan.mp3'
        if isfile(join(abspath(dirname(__file__)), 'audio_files', 'custom.mp3')):
            file_name = 'custom.mp3'
        elif self.settings.get('audio_file_path'):
            url = self.settings.get('audio_file_path')
            if self._valid_extension(url):
                file_name = url
            else:
                self.log.info('Error, Custom file must be mp3, using default.')
                self.speak_dialog("Only mp3 files are accepted. Using default.")
        else:
            self.log.info('Custom mp3 not found, using default.')
        self.audio_file = join(abspath(dirname(__file__)), 'audio_files', file_name)

    @intent_file_handler('noise.white.intent')
    def handle_noise_white(self, message):
        wait_while_speaking()
        self.speak_dialog('noise.white')
        wait_while_speaking()

        secs = None
        if message.data.get('duration', None):
            duration = message.data.get("duration")
            secs = self._extract_duration(duration)
        self.log.info("Playing " + self.audio_file)
        if isfile(self.audio_file):
            self.process = play_mp3(self.audio_file)
        else:
            self.log.error(self.audio_file + " not found.")
            self.speak_dialog("Audio file not found. Please try re-installing.")
            return

        if secs:
            self.kill = Process(target=self.kill_noise, args=(secs,))
            self.kill.start()

    def kill_noise(self, play_time):
        time.sleep(play_time)
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

    def download_default_audio_file(self, url):
        session = requests.Session()
        response = session.get(url, stream=True)

        file_name = 'custom.mp3'
        if not self._valid_extension(url):
            self.speak_dialog("Only mp3 files are accepted. Using default.")
            return

        with open(join(self.audio_dir, file_name), "wb") as f:
            for chunk in response.iter_content(2048):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

    @staticmethod
    def _valid_extension(url):
        file_name_split = splitext(url)
        ext = file_name_split[len(file_name_split) - 1].split('?')[0]
        if ext != '.mp3':
            return False
        return True

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()


def create_skill():
    return WhiteNoise()
