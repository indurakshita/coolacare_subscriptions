from rest_framework import serializers
from authapp.exception import CustomException
import re

class SubscriptionValidationSerializer(serializers.Serializer):
    dayname = serializers.ListField()
    session = serializers.ListField()
    time = serializers.ListField()
    mode_of_call = serializers.CharField()
    package = serializers.CharField()

    def validate(self, data):
        mode_of_call = data.get('mode_of_call')
        package = data.get('package')
        time_intervals = [
            "08:00 AM - 08:30 AM", "08:30 AM - 09:00 AM", "09:00 AM - 09:30 AM", "09:30 AM - 10:00 AM",
            "10:00 AM - 10:30 AM", "10:30 AM - 11:00 AM", "11:00 AM - 11:30 AM", "11:30 AM - 12:00 PM",
            "12:00 PM - 12:30 PM", "12:30 PM - 01:00 PM", "01:00 PM - 01:30 PM", "01:30 PM - 02:00 PM",
            "02:00 PM - 02:30 PM", "02:30 PM - 03:00 PM", "03:00 PM - 03:30 PM", "03:30 PM - 04:00 PM",
            "04:00 PM - 04:30 PM", "04:30 PM - 05:00 PM", "05:00 PM - 05:30 PM", "05:30 PM - 06:00 PM",
            "06:00 PM - 06:30 PM", "06:30 PM - 07:00 PM", "07:00 PM - 07:30 PM", "07:30 PM - 08:00 PM"
        ]
        session_time_ranges = {
            'Morning': (12, 16),
            'Afternoon': (16, 20),
            'Evening': (20, 24),
        }

        # Additional validation for the entire serializer
        valid_daynames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if not all(dayname in valid_daynames for dayname in data['dayname']):
            raise CustomException(detail=f"Invalid dayname. Must be one of: {', '.join(valid_daynames)}", status_code=400)

        valid_sessions = ['Morning', 'Afternoon', 'Evening']
        if not all(session in valid_sessions for session in data['session']):
            raise CustomException(detail=f"Invalid session. Must be one of: {', '.join(valid_sessions)}", status_code=400)
        
        if len(data['dayname']) > (7 if package == "PLATINUM" else 5):
                raise CustomException(detail=f"dayname should be less than or equel {7 if package == 'PLATINUM' else 5} for {package}", status_code=400)
        
        if package =="PLATINUM":
            if len(data['session']) >3:
                    raise CustomException(detail="Session list should inside 3 values for platinum", status_code=400)
            
            if len(data['time']) >3:
                    raise CustomException(detail="Time list should inside 3 values for platinum", status_code=400)
            
            if not data.get("session") or not data.get("time") or not data.get("dayname"):
                    raise CustomException(detail="session, time, or dayname should not be empty list", status_code=400)
            
            if len(data['session']) != len(data['time']):
                raise CustomException(detail="Lengths of session and time lists should be equal", status_code=400)
        
            if mode_of_call.upper() == 'VOICE':
                for time_value in data['time']:
                    if not re.match(r'^(0?[1-9]|1[0-2]):([03]0) (AM|PM) - (0?[1-9]|1[0-2]):([03]0) (AM|PM)$', time_value):
                        raise CustomException(detail="Invalid time format. Use format 'hh:00 AM/PM - hh:30 AM/PM' or 'hh:30 AM/PM - hh:00 AM/PM'", status_code=400)
                    
                    if time_value not in time_intervals:
                        raise CustomException(detail="Invalid time format. Time should be in 30-minute intervals from 08:00 AM to 08:00 PM", status_code=400)
                
                for session, time_value in zip(data['session'], data['time']):
                    # start_time, end_time = session_time_ranges[session]
                    time_parts = time_value.split(' - ')
                    start_time_parts = time_parts[0].split(':')
                    end_time_parts = time_parts[1].split(':')
                    start_hour, start_minute = int(start_time_parts[0]), start_time_parts[1]
                    end_hour, end_minute = int(end_time_parts[0]), end_time_parts[1]
                    if start_minute == end_minute:
                        raise CustomException(detail="Invalid minute values", status_code=400)
                    # if not (start_time <= start_hour <= end_hour <= end_time):
                    #     raise CustomException(detail=f"Invalid time range '{time_value}' for session '{session}'. Time should be between {start_time}:00 and {end_time}:00.", status_code=400)
            
            elif mode_of_call.upper() == 'SMS':
                for time_value in data['time']:
                    if not re.match(r'^\d{2}:\d{2}$', time_value):
                        raise CustomException(detail="Invalid time format for sms mode. Use format 'HH:MM'", status_code=400)

                for session, time_value in zip(data['session'], data['time']):
                    start_time, end_time = session_time_ranges[session]
                    time_hour = int(time_value.split(':')[0])
                    if not (start_time <= time_hour < end_time):
                        raise CustomException(detail=f"Invalid time '{time_value}' for session '{session}'. Time should be between {start_time}:00 and {end_time }:00.", status_code=400)
        
        if package =="GOLD":
            if not data.get("dayname"):
                raise CustomException(detail="dayname should not be empty list", status_code=400)
            
            if mode_of_call.upper() == 'VOICE':
                
                if not data.get("session") or not data.get("dayname"):
                    raise CustomException(detail="session or dayname should not be empty list", status_code=400)
                
                for time_value in data['time']:
                    if not re.match(r'^(0?[1-9]|1[0-2]):([03]0) (AM|PM) - (0?[1-9]|1[0-2]):([03]0) (AM|PM)$', time_value):
                        raise CustomException(detail="Invalid time format. Use format 'hh:00 AM/PM - hh:30 AM/PM' or 'hh:30 AM/PM - hh:00 AM/PM'", status_code=400)
        
                    if time_value not in time_intervals:
                        raise CustomException(detail="Invalid time format. Time should be in 30-minute intervals from 08:00 AM to 08:00 PM", status_code=400)
                    
                for session, time_value in zip(data['session'], data['time']):
                    time_parts = time_value.split(' - ')
                    start_time_parts = time_parts[0].split(':')
                    end_time_parts = time_parts[1].split(':')
                    start_hour, start_minute = int(start_time_parts[0]), start_time_parts[1]
                    end_hour, end_minute = int(end_time_parts[0]), end_time_parts[1]
                    if start_minute == end_minute:
                        raise CustomException(detail="Invalid minute values", status_code=400)
                    # if not (start_time <= start_hour <= end_hour <= end_time):
                    #     raise CustomException(detail=f"Invalid time range '{time_value}' for session '{session}'. Time should be between {start_time}:00 and {end_time}:00.", status_code=400)
            
            elif mode_of_call.upper() == 'SMS':
                
                if len(data['session']) >3:
                    raise CustomException(detail="Session list should inside 3 values for gold", status_code=400)
            
                if len(data['time']) >3:
                    raise CustomException(detail="Time list should be inside values for gold", status_code=400)
                
                if not data.get("session") or not data.get("time") or not data.get("dayname"):
                    raise CustomException(detail="session, time, or dayname should not be empty list", status_code=400)
                
                if len(data['session']) != len(data['time']):
                    raise CustomException(detail="Lengths of session and time lists should be equal", status_code=400)
        
                for time_value in data['time']:
                    if not re.match(r'^\d{2}:\d{2}$', time_value):
                        raise CustomException(detail="Invalid time format for sms mode. Use format 'HH:MM'", status_code=400)
                
                for session, time_value in zip(data['session'], data['time']):
                    start_time, end_time = session_time_ranges[session]
                    time_hour = int(time_value.split(':')[0])
                    if not (start_time <= time_hour < end_time):
                        raise CustomException(detail=f"Invalid time '{time_value}' for session '{session}'. Time should be between {start_time}:00 and {end_time }:00.", status_code=400)
        
        if package =="SILVER":
            if len(data['session']) >3:
                    raise CustomException(detail="Session list should be 1 value for silver ", status_code=400)
            
            if len(data['time']) >3:
                raise CustomException(detail="Time list should be 1 value for silver", status_code=400)

            if not data.get("session") or not data.get("time") or not data.get("dayname"):
                    raise CustomException(detail="session, time, or dayname should not be empty list", status_code=400)
            
            if len(data['session']) != len(data['time']):
                raise CustomException(detail="Lengths of session and time lists should be equal", status_code=400)
        
            for time_value in data['time']:
                if not re.match(r'^\d{2}:\d{2}$', time_value):
                    raise CustomException(detail="Invalid time format for sms mode. Use format 'HH:MM'", status_code=400)
                   
            for session, time_value in zip(data['session'], data['time']):
                start_time, end_time = session_time_ranges[session]
                time_hour = int(time_value.split(':')[0])
                if not (start_time <= time_hour < end_time):
                    raise CustomException(detail=f"Invalid time '{time_value}' for session '{session}'. Time should be between {start_time}:00 and {end_time }:00.", status_code=400)
        
        return data