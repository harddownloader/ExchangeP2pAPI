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
    CreateMarketOrderView,
)
from apps.partners.views import PartnersAPIList
from apps.googlesheets.views import (GSCreateTaskAPIView, GSConfigAPIView)
from .views import index

router = routers.DefaultRouter()
router.register(r'v1/p2p-orders', P2PMarketOrdersViewSet, basename='P2PMarketOrders')

API_PREFIX = 'api'

API_PREFIX_V1 = f'{API_PREFIX}/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),

    # google spreadsheet triggers
    path(f'{API_PREFIX_V1}/googlesheets/create-task', GSCreateTaskAPIView.as_view()),
    path(f'{API_PREFIX_V1}/googlesheets/triggers', GSConfigAPIView.as_view()),

    # jwt
    path(f'{API_PREFIX_V1}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX_V1}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'{API_PREFIX_V1}/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # orders
    path(f'{API_PREFIX}/', include(router.urls)),
    path(f'{API_PREFIX_V1}/orders', OrdersAPIList.as_view()),  # get all / post

    # for admin
    # for partner
    path(f'{API_PREFIX_V1}/orders/<int:pk>/', OrderAPIUpdate.as_view()),  # get,put,patch by id
    path(
        f'{API_PREFIX_V1}/ordersdelete/<int:pk>/',
        OrderAPIDestroy.as_view(),
        name='delete-orders'
    ),  # delete by id

    # partners (users)
    path(f'{API_PREFIX_V1}/partners', PartnersAPIList.as_view()),

    # market_monitor
    path(f'{API_PREFIX_V1}/marketmonitors', MarketMonitorCreateView.as_view(), name='market-monitor-list-create'),
    path(f'{API_PREFIX_V1}/marketmonitors/<int:pk>/', MarketMonitorsRetrieveUpdateDestroyView.as_view(), name='market-monitor-retrieve-update-destroy'),

    # markets
    path(f'{API_PREFIX_V1}/market', MarketsCreateView.as_view(), name='market-list-create'),
    path(f'{API_PREFIX_V1}/market/<int:pk>/', MarketsRetrieveUpdateDestroyView.as_view(), name='market-retrieve-update-destroy'),

    # market accounts
    path(f'{API_PREFIX_V1}/market-accounts', MarketAccountCreateView.as_view(), name='market-accounts-list-create'),
    path(f'{API_PREFIX_V1}/market-accounts/<int:pk>/', MarketAccountRetrieveUpdateDestroyView.as_view(), name='markets-accounts-retrieve-update-destroy'),

    # market orders
    path(f'{API_PREFIX_V1}/market-orders', CreateMarketOrderView.as_view(), name='market-orders-create'),

    # pay types
    path(f'{API_PREFIX_V1}/pay-types', PayTypesCreateView.as_view(), name='pay-types-list-create'),
    path(f'{API_PREFIX_V1}/pay-types/<int:pk>/', PayTypesAccountRetrieveUpdateDestroyView.as_view(), name='pay-types-retrieve-update-destroy'),

    # fiat
    path(f'{API_PREFIX_V1}/fiat', FiatCurrencyCreateView.as_view(), name='fiat-list-create'),
    path(f'{API_PREFIX_V1}/fiat/<int:pk>/', FiatCurrencyAccountRetrieveUpdateDestroyView.as_view(), name='fiat-retrieve-update-destroy'),
]
