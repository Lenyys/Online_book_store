from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        raise PermissionDenied  # 403 chyba