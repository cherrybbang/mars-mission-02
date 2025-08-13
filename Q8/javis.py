import os
import csv
import wave
import speech_recognition as sr
from datetime import datetime
import pandas as pd

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Q7의 records 폴더 경로 설정
        self.q7_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Q7")
        self.records_dir = os.path.join(self.q7_dir, "records")
        
        # Q8의 결과 저장 폴더
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(current_dir, "results")
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            print(f"'{self.results_dir}' 폴더를 생성했습니다.")
    
    def get_audio_files(self):
        """Q7/records 폴더의 음성파일 목록 가져오기"""
        if not os.path.exists(self.records_dir):
            print(f"Records 폴더가 존재하지 않습니다: {self.records_dir}")
            return []
        
        audio_files = []
        for filename in os.listdir(self.records_dir):
            if filename.endswith(('.wav', '.mp3', '.flac', '.aiff', '.aif')):
                file_path = os.path.join(self.records_dir, filename)
                audio_files.append(file_path)
        
        return sorted(audio_files)
    
    def get_audio_info(self, file_path):
        """오디오 파일의 정보 가져오기"""
        try:
            with wave.open(file_path, 'rb') as wf:
                frames = wf.getnframes()
                sample_rate = wf.getframerate()
                duration = frames / float(sample_rate)
                return {
                    'duration': round(duration, 2),
                    'sample_rate': sample_rate,
                    'frames': frames
                }
        except Exception as e:
            print(f"오디오 정보 읽기 오류 ({file_path}): {e}")
            return {'duration': 0, 'sample_rate': 0, 'frames': 0}
    
    def speech_to_text(self, file_path):
        """음성 파일을 텍스트로 변환"""
        try:
            # 음성 파일 로드
            with sr.AudioFile(file_path) as source:
                # 배경 소음 조정
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # 오디오 녹음
                audio_data = self.recognizer.record(source)
            
            # Google Speech Recognition 사용하여 음성을 텍스트로 변환
            text = self.recognizer.recognize_google(audio_data, language='ko-KR')
            return text
            
        except sr.UnknownValueError:
            return "[음성을 인식할 수 없음]"
        except sr.RequestError as e:
            return f"[Google Speech Recognition 서비스 오류: {e}]"
        except Exception as e:
            return f"[오류: {e}]"
    
    def process_all_files(self):
        """모든 음성 파일을 처리하여 텍스트 추출"""
        audio_files = self.get_audio_files()
        
        if not audio_files:
            print("처리할 음성 파일이 없습니다.")
            return []
        
        print(f"{len(audio_files)}개의 음성 파일을 찾았습니다.")
        
        results = []
        
        for i, file_path in enumerate(audio_files, 1):
            filename = os.path.basename(file_path)
            print(f"\n[{i}/{len(audio_files)}] 처리 중: {filename}")
            
            # 파일 정보 가져오기
            audio_info = self.get_audio_info(file_path)
            
            # 음성을 텍스트로 변환
            print("  음성 인식 중...")
            text = self.speech_to_text(file_path)
            
            # 결과 저장
            result = {
                'filename': filename,
                'file_path': file_path,
                'duration_seconds': audio_info['duration'],
                'sample_rate': audio_info['sample_rate'],
                'recognized_text': text,
                'processed_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_size_kb': round(os.path.getsize(file_path) / 1024, 2)
            }
            
            results.append(result)
            print(f"  인식된 텍스트: {text}")
        
        return results
    
    def save_to_csv(self, results, filename=None):
        """결과를 CSV 파일로 저장"""
        if not results:
            print("저장할 데이터가 없습니다.")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"speech_recognition_results_{timestamp}.csv"
        
        csv_path = os.path.join(self.results_dir, filename)
        
        try:
            # pandas를 사용하여 CSV 저장
            df = pd.DataFrame(results)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            print(f"\n결과가 CSV 파일로 저장되었습니다: {csv_path}")
            print(f"총 {len(results)}개의 음성 파일이 처리되었습니다.")
            
            # 저장된 데이터 요약 출력
            self.print_summary(results)
            
        except Exception as e:
            print(f"CSV 저장 중 오류 발생: {e}")
    
    def print_summary(self, results):
        """처리 결과 요약 출력"""
        print("\n=== 처리 결과 요약 ===")
        
        total_duration = sum(r['duration_seconds'] for r in results)
        total_size = sum(r['file_size_kb'] for r in results)
        
        recognized_count = len([r for r in results if not r['recognized_text'].startswith('[')])
        error_count = len(results) - recognized_count
        
        print(f"총 파일 수: {len(results)}")
        print(f"성공적으로 인식된 파일: {recognized_count}")
        print(f"인식 실패/오류 파일: {error_count}")
        print(f"총 음성 길이: {total_duration:.2f}초")
        print(f"총 파일 크기: {total_size:.2f}KB")
        
        if recognized_count > 0:
            print(f"인식 성공률: {(recognized_count/len(results)*100):.1f}%")
    
    def display_files_list(self):
        """음성 파일 목록 출력"""
        audio_files = self.get_audio_files()
        
        if not audio_files:
            print("Q7/records 폴더에 음성 파일이 없습니다.")
            return
        
        print(f"\n=== Q7/records 폴더의 음성 파일 목록 ===")
        for i, file_path in enumerate(audio_files, 1):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            audio_info = self.get_audio_info(file_path)
            
            print(f"{i}. {filename}")
            print(f"   크기: {file_size:.2f}KB")
            print(f"   길이: {audio_info['duration']}초")
            print(f"   샘플레이트: {audio_info['sample_rate']}Hz")

def main():
    stt = SpeechToText()
    
    while True:
        print("\n=== JAVIS Speech-to-Text 변환기 ===")
        print("1. Q7/records 폴더의 음성 파일 목록 보기")
        print("2. 모든 음성 파일 텍스트 변환 및 CSV 저장")
        print("3. 특정 파일 텍스트 변환")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ").strip()
        
        if choice == "1":
            stt.display_files_list()
            
        elif choice == "2":
            print("\n모든 음성 파일을 처리합니다...")
            print("※ 인터넷 연결이 필요합니다 (Google Speech Recognition 사용)")
            
            confirm = input("계속하시겠습니까? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                results = stt.process_all_files()
                if results:
                    stt.save_to_csv(results)
            
        elif choice == "3":
            audio_files = stt.get_audio_files()
            if not audio_files:
                print("처리할 음성 파일이 없습니다.")
                continue
                
            print("\n음성 파일 목록:")
            for i, file_path in enumerate(audio_files, 1):
                filename = os.path.basename(file_path)
                print(f"{i}. {filename}")
            
            try:
                file_idx = int(input("변환할 파일 번호를 선택하세요: ")) - 1
                if 0 <= file_idx < len(audio_files):
                    file_path = audio_files[file_idx]
                    filename = os.path.basename(file_path)
                    print(f"\n'{filename}' 처리 중...")
                    
                    text = stt.speech_to_text(file_path)
                    print(f"인식된 텍스트: {text}")
                else:
                    print("올바른 파일 번호를 입력해주세요.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
                
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
            
        else:
            print("올바른 번호를 선택해주세요.")

if __name__ == "__main__":
    main()