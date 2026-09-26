import sys
import logging

def error_message_detail(error:Exception , error_detail:sys)->str:
      """
      extracts detailed error information including file name , number and error msg.
      param 1 -> the exception that occurred.
      param 2 -> the sys module to access traceback detail
      return -> a formatted error msg string 
      """
      
      # extract trace back details (exception information)
      _, _, exc_tb = error_detail.exc_info()
      
      # get the file name , and line no. where the exception occurred
      file_name = exc_tb.tb_frame.f_code.co_filename
      line_number = exc_tb.tb_lineno
      
      # create formatted error msg
      error_message = f"error occurred in python script: [{file_name} at line no.{line_number}]: {str(error)}"
      
      logging.error(error_message)
      
      return error_message

class MyException(Exception):
      """
      Custom exception class for handling error for getting error in custome format manner
      """
      
      def __init__(self , error_message:str , error_detail:sys ):
            """
            initialize myexception class with error msg and its detail
            """
            # calling the parent class constructor
            super().__init__(error_message)
            
            self.error_message = error_message_detail(error_message,error_detail)
            
      def __str__(self)->str:
            """
            return string format of the message
            """
            return self.error_message

            
            
            
            
            
      
       