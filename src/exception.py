import sys
#import logging
def error_message(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    line_number = exc_tb.tb_lineno
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_msg = f"Error occurred in script: {file_name} at line number: {line_number} with message: {str(error)}"
    return error_msg

class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message(error_message,error_detail=error_details)

    def __str__(self):
        return self.error_message
    

if __name__=="__main__":
    try:
        a = 1/0
    except Exception as e:
        raise CustomException(e,sys)
        
