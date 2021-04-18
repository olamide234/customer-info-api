"""customer_basee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from pivots.views import CustomerViewSet, ProfessionsViewSet, DataSheetViewSet, DocumentViewSet

# router = routers.DefaultRouter()  
# router.register('users', UserViewSet, 'user')  
# router.register('accounts', AccountViewSet, 'account')  
  
# urlpatterns = router.urls 
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'professionss', ProfessionsViewSet)
router.register(r'data_sheets', DataSheetViewSet)
router.register(r'documents', DocumentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]

# {
#     "name": "Cain",
#     "address": "20, Eleyele",
#     "profession": [
#         {
#             "description": "Affiliate marketer"
#         }
#     ],
#     "data_sheet": {
#         "id": 9,
#         "description": "Cain historical data sheet",
#         "historical_data": "datasheet"
#     },
#     "active": true,
#     "document_set": [
#         {
#         "dtype": "PP",
#         "doc_number": "CD-9877",
#         "documents": "Cain"
#         }
#     ]
# }