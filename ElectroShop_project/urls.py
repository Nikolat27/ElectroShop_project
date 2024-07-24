from django.contrib import admin
from django.urls import path, include
from account_app.models import User
from . import settings
from django.conf.urls.static import static
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('products/', include("product_app.urls")),
                  path('accounts/', include("account_app.urls")),
                  path('cart/', include("cart_app.urls")),
                  path('', include("home_app.urls")),
                  path('', include("captcha.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
