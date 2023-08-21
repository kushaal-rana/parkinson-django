from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import h5py
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
import pandas as pd
import sys
import os
from rest_framework.views import APIView


class ExecutionScriptAPI(APIView):
    def __init__(self) -> None:
        return None

    def post(self, request) -> Response:
        try:
            fileName = request.FILES["file"]
            if fileName:
                f = h5py.File(fileName, 'r')  # name of the file from which data is being extracted
                # use these loops to get the key names
                csv_links = []
                for group in f.keys():
                    if group == "Sensors":
                        for dset in f[group]:
                            print("-", type(dset))
                            print("Extracting data................")
                            accel = list(f['Sensors'][dset]['Accelerometer'])
                            gyro = list(f['Sensors'][dset]['Gyroscope'])
                            time = list(f['Sensors'][dset]['Time'])
                            # Time is in string, you will have to convert to timestamps
                            time = [datetime.fromtimestamp(x / 1000000) for x in time]

                            x_accel = []
                            y_accel = []
                            z_accel = []

                            # Extract values from the list of arrays
                            for array in accel:
                                x_accel.append(array[0])
                                y_accel.append(array[1])
                                z_accel.append(array[2])

                            x_gyro = []
                            y_gyro = []
                            z_gyro = []

                            # Extract values from the list of arrays
                            for array in gyro:
                                x_gyro.append(array[0])
                                y_gyro.append(array[1])
                                z_gyro.append(array[2])

                            df = pd.DataFrame({
                                'time': time,
                                'x_accel': x_accel,
                                'y_accel': y_accel,
                                'z_accel': z_accel,
                                'x_gyro': x_gyro,
                                'z_gyro': z_gyro,
                                'y_gyro': y_gyro
                            })
                            csv_filename = f'data_{dset}_new.csv'
                            csv_filepath = os.path.join('.', csv_filename)
                            result = "CSV file(s) saved"
                            df.to_csv(csv_filepath, index=False)
                            print("File converted successfully")
                            csv_links.append(csv_filename)
                            
                return Response({"result": "CSV file(s) processed", "csv_data": csv_links}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Missing or invalid filename"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCsv(APIView):
    def __init__(self) -> None:
        return None
        
    def get(self,request,filename):
        try:
            csv_filepath = os.path.join('.', filename)
  
            if os.path.exists(csv_filepath):
                with open(csv_filepath, 'r') as csv_file:
                    csv_content = csv_file.read()
                    return Response({"content": csv_content})
            else:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
  