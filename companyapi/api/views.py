
from rest_framework.response import Response
from rest_framework.decorators import action,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from rest_framework.exceptions import PermissionDenied
from api.models import Patient, Prescription, User
from api.serializers import PatientSerializer, PrescriptionSerializer,UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  # Add this import

from rest_framework.permissions import BasePermission
from rest_framework import viewsets




@api_view(['POST'])
def register_user(request):
    """
    Registers a new user (admin, doctor, read_only)
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom Permissions
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET'] and request.user.is_authenticated and request.user.role == 'read_only'






# ViewSet for managing Patient profiles
class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Patient profiles.
    Allows CRUD operations for the Patient model.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    #permission_classes = [IsDoctor, IsAdmin,IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    permission_classes = [IsAuthenticated]  # Allow access to authenticated users

    def get_queryset(self):
        """
        Restrict queryset based on user roles.
        """
        user = self.request.user
        if user.role == "doctor":
            # Doctors can view all patients
            return Patient.objects.all()
        elif user.role == "admin":
            # Admins can view all patients
            return Patient.objects.all()
        elif user.role == "read_only":
            # Read-only users cannot modify patients
            return Patient.objects.all()
        raise PermissionDenied("Invalid role.")

    def perform_create(self, serializer):
        """
        Automatically link the created patient to the logged-in user (if applicable).
        """
        user = self.request.user
        if user.role != "doctor":
            raise PermissionDenied("Only doctors can create patient profiles.")
        serializer.save()

    @action(detail=True, methods=['get'], url_path='medical-history')
    def medical_history(self, request, pk=None):
        """
        Retrieves medical history (prescriptions) for a specific patient.
        """
        patient = self.get_object()
        prescriptions = Prescription.objects.filter(patient=patient)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'], url_path='prescriptions')
    def get_prescriptions(self, request, pk=None):
        """
        Retrieves a list of prescriptions for a specific patient.
        """
        patient = self.get_object()
        prescriptions = Prescription.objects.filter(patient=patient)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
        
@action(detail=True, methods=['get'], url_path='medical-history')
def medical_history(self, request, pk=None):
    """
    Retrieves medical history (prescriptions) for a specific patient.
    """
    patient = self.get_object()
    prescriptions = Prescription.objects.filter(patient=patient)
    # Pass the request object in the context
    serializer = PrescriptionSerializer(prescriptions, many=True, context={'request': request})
    return Response(serializer.data)


# ViewSet for managing Prescriptions
class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Prescriptions.
    Allows CRUD operations for the Prescription model.
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Restrict queryset based on user roles.
        """
        user = self.request.user
        if user.role in ["doctor", "admin"]:
            # Doctors and Admins can view all prescriptions
            return Prescription.objects.all()
        elif user.role == "read_only":
            # Read-only users can view prescriptions but not modify
            return Prescription.objects.all()
        raise PermissionDenied("Invalid role.")

    def perform_create(self, serializer):
        """
        Automatically link the created prescription to the logged-in user and patient.
        """
        user = self.request.user
        if user.role != "doctor":
            raise PermissionDenied("Only doctors can create prescriptions.")
        serializer.save()

    @action(detail=True, methods=['post'], url_path='renew', url_name='renew-prescription')
    def renew_prescription(self, request, pk=None):
        """
        Renews an existing prescription by duplicating it with a new status and/or updated details.
        """
        prescription = self.get_object()
        renewed_prescription = Prescription.objects.create(
            patient=prescription.patient,
            medication_details=prescription.medication_details,
            dosage=prescription.dosage,
            duration=prescription.duration,
            status='active',
            renewed_from=prescription
        )
        serializer = PrescriptionSerializer(renewed_prescription)
        return Response(serializer.data, status=201)
