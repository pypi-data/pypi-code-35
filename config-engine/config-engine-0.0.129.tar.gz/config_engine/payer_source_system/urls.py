from django.conf.urls import url

from config_engine.payer_source_system import views

urlpatterns = [
    url(r'^$', views.PayerSourceSystemList.as_view(), name='config'),
    # url(r'^config/(?P<pk>\d+)/$', views.PayerSourceSystemConfigDetailView.as_view(), name='config_detail'),
    url(r'^payer/$', views.PayerList.as_view(), name='payer_list'),
    # url(r'^payer/(?P<pk>\d+)/$', views.PayerDetailView.as_view(), name='config_engine_payer_detail'),
    url(r'^product/$', views.ProductList.as_view(), name='product_list'),
    # url(r'^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='config_engine_product_detail')
    url(r'^product-feature/$', views.CXProductFeatureList.as_view(), name='product_feature_list'),

]
