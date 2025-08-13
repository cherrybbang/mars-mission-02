import pyaudio
import wave
import os
import threading
from datetime import datetime

class VoiceRecorder:
    def __init__(self):
        # 오디오 설정
        self.chunk = 1024  # 버퍼 크기
        self.format = pyaudio.paInt16  # 16비트 오디오
        self.channels = 1  # 모노 채널
        self.rate = 44100  # 샘플링 레이트 44.1kHz
        
        # PyAudio 객체
        self.audio = pyaudio.PyAudio()
        
        # 녹음 상태
        self.is_recording = False
        self.frames = []
        
        # records 폴더 생성
        self.records_dir = "records"
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)
            print(f"'{self.records_dir}' 폴더를 생성했습니다.")
    
    def get_available_devices(self):
        """사용 가능한 오디오 장치 목록 출력"""
        print("\n=== 사용 가능한 오디오 장치 목록 ===")
        device_count = self.audio.get_device_count()
        
        for i in range(device_count):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:  # 입력 장치만 표시
                print(f"Device {i}: {device_info['name']} - {device_info['maxInputChannels']} channels")
        print("=" * 40)
    
    def get_filename(self):
        """현재 날짜와 시간을 기반으로 파일명 생성"""
        now = datetime.now()
        filename = now.strftime("%Y%m%d-%H%M%S.wav")
        return os.path.join(self.records_dir, filename)
    
    def start_recording(self, device_index=None):
        """녹음 시작"""
        if self.is_recording:
            print("이미 녹음 중입니다.")
            return
        
        try:
            # 스트림 열기
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk
            )
            
            self.is_recording = True
            self.frames = []
            
            print("녹음을 시작합니다... (Enter를 눌러 중지)")
            
            # 별도 스레드에서 녹음 실행
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.start()
            
        except Exception as e:
            print(f"녹음 시작 중 오류 발생: {e}")
            self.is_recording = False
    
    def _record(self):
        """실제 녹음 수행 (별도 스레드에서 실행)"""
        try:
            while self.is_recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
        except Exception as e:
            print(f"녹음 중 오류 발생: {e}")
        finally:
            if hasattr(self, 'stream'):
                self.stream.stop_stream()
                self.stream.close()
    
    def stop_recording(self):
        """녹음 중지 및 파일 저장"""
        if not self.is_recording:
            print("녹음이 진행 중이 아닙니다.")
            return
        
        print("녹음을 중지합니다...")
        self.is_recording = False
        
        # 녹음 스레드가 종료될 때까지 대기
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join()
        
        # 파일 저장
        filename = self.get_filename()
        self._save_audio_file(filename)
        
        print(f"녹음이 완료되었습니다: {filename}")
    
    def _save_audio_file(self, filename):
        """녹음된 오디오를 WAV 파일로 저장"""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    
    def record_with_duration(self, duration_seconds, device_index=None):
        """지정된 시간 동안 녹음"""
        if self.is_recording:
            print("이미 녹음 중입니다.")
            return
        
        try:
            # 스트림 열기
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk
            )
            
            print(f"{duration_seconds}초 동안 녹음합니다...")
            
            frames = []
            for i in range(0, int(self.rate / self.chunk * duration_seconds)):
                data = stream.read(self.chunk)
                frames.append(data)
                
                # 진행률 표시
                progress = (i + 1) / int(self.rate / self.chunk * duration_seconds) * 100
                print(f"\r녹음 진행률: {progress:.1f}%", end="")
            
            print("\n녹음 완료!")
            
            # 스트림 정리
            stream.stop_stream()
            stream.close()
            
            # 파일 저장
            filename = self.get_filename()
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            
            print(f"파일이 저장되었습니다: {filename}")
            
        except Exception as e:
            print(f"녹음 중 오류 발생: {e}")
    
    def cleanup(self):
        """PyAudio 객체 정리"""
        if hasattr(self, 'audio'):
            self.audio.terminate()

def main():
    recorder = VoiceRecorder()
    
    try:
        while True:
            print("\n=== JAVIS 음성 녹음기 ===")
            print("1. 사용 가능한 마이크 장치 보기")
            print("2. 수동 녹음 시작/중지")
            print("3. 시간 지정 녹음")
            print("4. 종료")
            
            choice = input("\n선택하세요 (1-4): ").strip()
            
            if choice == "1":
                recorder.get_available_devices()
                
            elif choice == "2":
                if not recorder.is_recording:
                    device_input = input("마이크 장치 번호 (기본값은 Enter): ").strip()
                    device_index = int(device_input) if device_input.isdigit() else None
                    
                    recorder.start_recording(device_index)
                    input()  # Enter 키 대기
                    recorder.stop_recording()
                else:
                    recorder.stop_recording()
                    
            elif choice == "3":
                try:
                    duration = float(input("녹음 시간을 초 단위로 입력하세요: "))
                    device_input = input("마이크 장치 번호 (기본값은 Enter): ").strip()
                    device_index = int(device_input) if device_input.isdigit() else None
                    
                    recorder.record_with_duration(duration, device_index)
                except ValueError:
                    print("올바른 숫자를 입력해주세요.")
                    
            elif choice == "4":
                print("프로그램을 종료합니다.")
                break
                
            else:
                print("올바른 번호를 선택해주세요.")
                
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    finally:
        recorder.cleanup()

if __name__ == "__main__":
    main()