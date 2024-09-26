from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Class 
from School.models import *
from .serializer import ClassSerializer
from School.utils.authCheck import *
from django.utils.decorators import method_decorator

class DefineClasses(APIView):
    @method_decorator(is_school_logged_in)
    def post(self, request):
        school_id = request.school.school_id
        try:
            school = School.objects.get(school_id=school_id)
            print(school)
            if school.classes_defined:
                return Response({'message': 'Classes are already defined.'}, status=status.HTTP_400_BAD_REQUEST)

            class_type = request.data.get('class_type')
            if class_type == 'nursery_to_tenth':
                standards = ['Nursery', 'Jr_KG', 'Sr_KG', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth']
            elif class_type == 'first_to_tenth':
                standards = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth']
            elif class_type == 'custom':
                standards = request.data.get('standards')  # Expecting a list of standards from the request
            else:
                return Response({'error': 'Invalid class type selected.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create classes with default division 'A'
            for standard in standards:
                class_obj = Class(
                    class_std=standard,
                    class_division='A',
                    school_id=school
                )
                class_obj.save()

            school.classes_defined = True
            school.save()

            return Response({'message': 'Classes defined successfully Humaira.'}, status=status.HTTP_200_OK)

        except School.DoesNotExist:
            return Response({'error': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddDivision(APIView):
    def post(self, request):
        school_id = request.user.school_id
        standard = request.data.get('standard')  # The standard to which the division is being added
        try:
            school = School.objects.get(school_id=school_id)
            existing_classes = Class.objects.filter(school=school, class_std=standard).order_by('class_division')
            
            if not existing_classes.exists():
                return Response({'error': 'Standard not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            last_division = existing_classes.last().class_division  # Get the last division created
            new_division = chr(ord(last_division) + 1)  # Calculate the next division (e.g., 'A' -> 'B')
            
            new_class = Class(
                class_std=standard,
                class_division=new_division,
                school=school
            )
            new_class.save()

            return Response({'message': f'Division {new_division} added successfully to standard {standard}.'}, status=status.HTTP_200_OK)

        except School.DoesNotExist:
            return Response({'error': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateStandardsView(APIView):
    def put(self, request):
        school_id = request.user.school_id  # Assuming you have the school ID from the logged-in user
        try:
            school = School.objects.get(school_id=school_id)
            if not school.classes_defined:
                return Response({'message': 'Classes are not yet defined. Please define them first.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the update type from the request data
            update_type = request.data.get('update_type')
            if update_type == 'roman':
                roman_standards = {
                    'First': 'I', 'Second': 'II', 'Third': 'III', 'Fourth': 'IV', 'Fifth': 'V',
                    'Sixth': 'VI', 'Seventh': 'VII', 'Eighth': 'VIII', 'Ninth': 'IX', 'Tenth': 'X'
                }
                for class_obj in Class.objects.filter(school=school):
                    if class_obj.class_std in roman_standards:
                        class_obj.class_std = roman_standards[class_obj.class_std]
                        class_obj.save()

                return Response({'message': 'Standards updated to Roman numerals successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid update type.'}, status=status.HTTP_400_BAD_REQUEST)

        except School.DoesNotExist:
            return Response({'error': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)