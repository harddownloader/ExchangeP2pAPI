"""
URL configuration for djangoP2pExchangeApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

# jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# views
from apps.market_monitors.views import (
    MarketMonitorCreateView,
    MarketMonitorsRetrieveUpdateDestroyView,
    P2PMarketOrdersViewSet,
)
from apps.markets.views import (
    MarketAccountCreateView,
    MarketsCreateView,
    MarketsRetrieveUpdateDestroyView,
    MarketAccountRetrieveUpdateDestroyView,
    PayTypesCreateView,
    PayTypesAccountRetrieveUpdateDestroyView,
    FiatCurrencyCreateView,
    FiatCurrencyAccountRetrieveUpdateDestroyView
)
from apps.orders.views import (
    OrdersAPIList,
    OrderAPIUpdate,
    OrderAPIDestroy,
)
from apps.partners.views import PartnersAPIList
from .views import index

router = routers.DefaultRouter()
router.register(r'v1/p2p-orders', P2PMarketOrdersViewSet, basename='P2PMarketOrders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),

    # jwt
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # orders
    path('api/', include(router.urls)),
    path('api/v1/orders', OrdersAPIList.as_view()),  # get all / post

    # for admin
    # for partner
    path('api/v1/orders/<int:pk>/', OrderAPIUpdate.as_view()),  # get,put,patch by id
    path(
        'api/v1/ordersdelete/<int:pk>/',
        OrderAPIDestroy.as_view(),
        name='delete-orders'
    ),  # delete by id

    # partners (users)
    path('api/v1/partners', PartnersAPIList.as_view()),

    # market_monitor
    path('api/v1/marketmonitors', MarketMonitorCreateView.as_view(), name='market-monitor-list-create'),
    path('api/v1/marketmonitors/<int:pk>/', MarketMonitorsRetrieveUpdateDestroyView.as_view(), name='market-monitor-retrieve-update-destroy'),

    # markets
    path('api/v1/market', MarketsCreateView.as_view(), name='market-list-create'),
    path('api/v1/market/<int:pk>/', MarketsRetrieveUpdateDestroyView.as_view(), name='market-retrieve-update-destroy'),

    # market accounts
    path('api/v1/market-accounts', MarketAccountCreateView.as_view(), name='market-accounts-list-create'),
    path('api/v1/market-accounts/<int:pk>/', MarketAccountRetrieveUpdateDestroyView.as_view(), name='markets-accounts-retrieve-update-destroy'),

    # pay types
    path('api/v1/pay-types', PayTypesCreateView.as_view(), name='pay-types-list-create'),
    path('api/v1/pay-types/<int:pk>/', PayTypesAccountRetrieveUpdateDestroyView.as_view(), name='pay-types-retrieve-update-destroy'),

    # fiat
    path('api/v1/fiat', FiatCurrencyCreateView.as_view(), name='fiat-list-create'),
    path('api/v1/fiat/<int:pk>/', FiatCurrencyAccountRetrieveUpdateDestroyView.as_view(), name='fiat-retrieve-update-destroy'),
]
