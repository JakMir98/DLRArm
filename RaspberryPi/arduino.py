import serial
import pytesseract

global arduino
arduino = serial.Serial("COM12", 9600)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\pawel\\Desktop\\tess\\tesseract.exe'
