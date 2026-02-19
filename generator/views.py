from typing import Any, Dict, List
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from faker import Faker
import csv
import io
import json
import re

from .models import Schema
from .serializers import SchemaSerializer, UserSerializer

SUPPORTED_DATA_TYPES = {
    "full_name": lambda f: f.name(), "first_name": lambda f: f.first_name(),
    "last_name": lambda f: f.last_name(), "email": lambda f: f.email(),
    "city": lambda f: f.city(), "country": lambda f: f.country(),
    "address": lambda f: f.address().replace("\n", ", "), "phone": lambda f: f.phone_number(),
    "company": lambda f: f.company(), "job": lambda f: f.job(), "uuid": lambda f: f.uuid4(),
    "date": lambda f: f.date(), "datetime": lambda f: f.iso8601(),
    "integer": lambda f: f.random_int(min=0, max=10000),
    "float": lambda f: round(f.pyfloat(left_digits=3, right_digits=3, positive=True), 3),
    "boolean": lambda f: f.pybool(),
}
def generate_rows(definition: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    faker = Faker()
    rows: List[Dict[str, Any]] = []
    for _ in range(count):
        record: Dict[str, Any] = {}
        for field in definition:
            field_name, data_type = field.get("field_name"), field.get("data_type")
            generator = SUPPORTED_DATA_TYPES.get(data_type)
            record[field_name] = generator(faker) if generator else None
        rows.append(record)
    return rows
def slugify_filename(name):
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    return re.sub(r'[-\s]+', '_', name)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class SchemaViewSet(viewsets.ModelViewSet):
    serializer_class = SchemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user).order_by("-updated_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@require_GET
def schema_download_view(request, pk: int):
    schema = get_object_or_404(Schema, pk=pk)
    fmt = request.GET.get("format", "csv").lower()
    count = schema.row_count
    data = generate_rows(schema.definition, count)
    safe_filename = slugify_filename(schema.name)

    if fmt == "json":
        content = json.dumps(data, indent=2, ensure_ascii=False)
        response = HttpResponse(content, content_type="application/json")
        filename = f"{safe_filename}.json"
    else:
        output = io.StringIO()
        fieldnames = [item.get("field_name") for item in schema.definition] if not data else list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        filename = f"{safe_filename}.csv"
        
    response["Content-Disposition"] = f"attachment; filename=\"{filename}\""
    return response