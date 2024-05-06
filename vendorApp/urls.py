from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # templates
    path('', views.home, name="home"), 
    
    # Token for Authenticated User (POST method)
    path('api-token-auth/', obtain_auth_token), 

    # 1. Vendor Profile Management:
    path('api/vendors/', views.VendorListView.as_view()),
    path('api/vendors/<int:pk>/', views.VendorView.as_view()),

    # 2. Purchase Order Tracking:
    path('api/purchase_orders/', views.Purchase_OrderListView.as_view()),
    path('api/purchase_orders/<int:pk>/', views.Purchase_OrderView.as_view()),
    path('api/purchase_orders/<int:pk>/acknowledge/', views.Purchase_Order_AcknowledgeView.as_view()),

    # 3. Vendor Performance Evaluation:
    path('api/vendors/<int:pk>/performance/', views.Vendor_Performance.as_view()),
] 



    # 1. Vendor Profile Management:

    #  POST /api/vendors/: Create a new vendor.
    #  GET /api/vendors/: List all vendors.
    #  GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    #  PUT /api/vendors/{vendor_id}/: Update a vendor's details.
    #  DELETE /api/vendors/{vendor_id}/: Delete a vendor.

    # 2. Purchase Order Tracking:

    #  POST /api/purchase_orders/: Create a purchase order.
    #  GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
    #  GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    #  PUT /api/purchase_orders/{po_id}/: Update a purchase order.
    #  DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
    
    # 3. Vendor Performance Evaluation:
    #  GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics


    # API Endpoint Implementation
    #  - Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):
    #  - Retrieves the calculated performance metrics for a specific vendor.
    #  - Should return data including on_time_delivery_rate, quality_rating_avg,
    #    average_response_time, and fulfillment_rate.
    
    # Update Acknowledgment Endpoint:
    #  - While not explicitly detailed in the previous sections, consider an endpoint like
    #  - POST /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge POs.
    #  - This endpoint will update acknowledgment_date and trigger the recalculation
    #    of average_response_time