from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        )


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUser"
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        )
        read_only_fields = ("id", "email", "password")
