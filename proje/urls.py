"""Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app2.views import signup, logout_user, login_user


from app.views import (
    index,
    product_detail,
    add_to_cart,
    cart_view,
    remove_from_cart,
)


from proje import settings

urlpatterns = [

  path('', index, name='index'),
  
  path('admin/', admin.site.urls),

  path('signup/', signup, name='signup'),
  
  path('logout/', logout_user, name='logout'),
  
  path('login/', login_user, name='login'),
  
  path('product/<str:slug>/', product_detail, name="product"),

  
  path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),

  path("", index, name="index"),
    path("admin/", admin.site.urls),

    path("cart/", cart_view, name="cart"),
    path("cart/remove/<int:product_id>/",
         remove_from_cart, name="remove_from_cart"),
    path("product/<str:slug>/add-to-cart/",
         add_to_cart, name="add_to_cart"),
    path("product/<str:slug>/",
         product_detail, name="product"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
