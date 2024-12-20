from rest_framework import serializers
from api.models import Patient, Prescription
from django.contrib.auth import get_user_model



User = get_user_model()  # This retrieves the custom User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Pop the password field
        user = User(**validated_data)  # Create the user instance
        user.set_password(password)  # Set the password securely
        user.save()  # Save the user to the database
        return user

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    # You can add custom fields or methods here based on the role
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        """
        Control the fields that should be serialized based on user role.
        For example, if the user is a doctor, return all fields.
        If the user is read-only, hide sensitive data like medical history.
        """
        representation = super().to_representation(instance)
        user = self.context.get('request').user  # Access the current logged-in user

        # If the user is 'read_only', exclude sensitive data like 'medical_history'
        if user.role == 'read_only':
            representation.pop('medical_history', None)

        return representation
    
def to_representation(self, instance):
    representation = super().to_representation(instance)
    user = self.context.get('request').user if self.context.get('request') else None
    if user:
        representation['user'] = user.username  # Example usage
    return representation
    

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

    def validate(self, data):
        """
        Ensure that the patient field is not null.
        Additionally, validate that only doctors can create prescriptions.
        """
        if not data.get('patient'):
            raise serializers.ValidationError({'patient': 'This field is required.'})
        
        # Check if the logged-in user is a doctor while creating the prescription
        user = self.context.get('request').user
        if user.role != 'doctor' and self.context.get('view').action == 'create':
            raise serializers.ValidationError("Only doctors can create prescriptions.")

        return data


