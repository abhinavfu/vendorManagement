from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import *
from .serializers import *
import json
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.

def home(request):
    """
    Home View renders template for home page when URL be requested by the user.
    """
    return render(request,'home.html')

# User Token Generation
for user in User.objects.all():
    Token.objects.get_or_create(user=user)


# Class Based API views

@permission_classes([IsAuthenticated])
class VendorListView(generics.ListCreateAPIView):
    """
    Clased Based Vendor List API view.
    Using Token based authentication, user can have access to get list of all vendors or can create a new vendor.

    Users can create a new vendor with following fields
            - name : vendor's name
            - contact_details : vendor's contact details
            - address : vendor's address
            - vendor_code : must be unique
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
        
    
@permission_classes([IsAuthenticated])
class VendorView(generics.RetrieveUpdateDestroyAPIView):
    """
    Clased Based Vendor Single item API view can retrieve single vendor 
    or can update single vendor or can Delete the particular vendor.
    
    Retrieve details of a specific Vendor or list all Vendors.

    Parameters:
        - self : represents the instance of the class.
        - request : object that contains metadata about the request.
        - pk (int): Vendor's id.
        - args (tuple): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

    Returns:
        Response: JSON response containing details of the specified Vendor(s).

    Raises:
        Exception: If the Vendor credentials were not specified.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
   
    def update(self, request,pk, *args, **kwargs):
        """
        Only Vendors can update their basic informations with following fields
            - name : update vendor's name
            - contact_details : update vendor's contact details
            - address : update vendor's address
        """
        try:
            vendors = Vendor.objects.get(name = self.request.user)
            vendor = Vendor.objects.get(id=pk)
            # if user is Vendor then Vendor can update their information, else will get some response
            if vendors == vendor:
                data = {}
                data['name'] = request.data["name"]
                data['contact_details'] = request.data["contact_details"]
                data['address'] = request.data["address"]
                serializer = VendorSerializer(vendor,data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"response":serializer.data,"message":"Updated successfully."},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response":"","message":"You are not same Vendor for this querry."},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"response":f"Required field - {str(e)}","message":"You are not Vendor or ERROR"},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request,pk, *args, **kwargs):
        """
        Only Admin can delete Vendor's record.
        """
        try:
            if self.request.user.is_superuser:
                vendor = Vendor.objects.get(id=pk)
                vendor.delete()
                return Response({"response":"","message":"Vendor deleted successfully."},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response":"","message":"You are not Admin."},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"response":str(e),"message":"You are not Admin."},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class Vendor_Performance(generics.RetrieveAPIView):
    """
    Clased Based Vendor Performance API view can retrieve vendor's performance metrics.
    """
    queryset = Vendor.objects.all()
    serializer_class = Vendor_PerformanceSerializer


@permission_classes([IsAuthenticated])
class Purchase_OrderListView(generics.ListCreateAPIView):
    """
    Purchase Order API view can get list of Purchase Order(s) or
    can create a new Purchase Order.

    Parameters:
        - self : represents the instance of the class.
        - request : object that contains metadata about the request.
        - args (tuple): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

    Returns:
        Response: JSON response containing details of the specified Purchase Order(s).

    Raises:
        Exception: If the Purchase Order credentials were not specified.
    """
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        User can create a new Purchase Order with following fields
            - po_number : must be unique
            - vendor : select one vendor using vendor_id
            - items : should be in dictionary
            - quantity : should be positive integer 
        """
        try:
            try:
                # check if user is vendor or not.
                is_vendor = Vendor.objects.get(name=self.request.user)
                is_vendor = True
            except:
                is_vendor = False
            # vendor  can't create Purchase Order
            if not is_vendor:
                data = {}
                data['po_number'] = request.data["po_number"]
                data['vendor'] = request.data["vendor"]
                data['order_date'] = datetime.now()
                # expected delivery date is 5 days
                data['delivery_date'] = datetime.today() + timedelta(days=5)
                try:
                    # if items is not in dict type it will throw error
                    data['items'] = json.loads(request.data["items"])
                except:raise ValidationError("items must be in dictionary, eg- {'name':'item name'}")

                data['quantity'] = request.data["quantity"]
                data['status'] = "pending"
                data['issue_date'] = datetime.now()
                
                serializer = Purchase_OrderSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"response":serializer.data,"message":"Order placed successfully."},status=status.HTTP_201_CREATED)
            else:
                return Response({"response":"","message":"Only user can placed a new purchase order."},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"response":f"Required field - {str(e)}","message":"ERROR"},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class Purchase_OrderView(generics.RetrieveUpdateDestroyAPIView):
    """
    Purchase Order API view can retrieve single Purchase Order or
    can update or delete single Purchase Order.

    Parameters:
        - self : represents the instance of the class.
        - request : object that contains metadata about the request.
        - pk (int): Purchase Order's id.
        - args (tuple): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

    Returns:
        Response: JSON response containing details of the specified Purchase Order(s).

    Raises:
        Exception: If the Purchase Order credentials were not specified.
    """
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_OrderSerializer
    
    def update(self, request,pk, *args, **kwargs):
        """
        User can update a selected Purchase Order with following fields
            - items : should be in dictionary
            - status : cancelled (User) or placed (vendor) 
        """
        try:
            obj_PO = Purchase_Order.objects.get(id=pk)
            data = {}
            try:
                # check if user is vendor or not.
                is_vendor = Vendor.objects.get(name=self.request.user)
                is_vendor = True
            except:
                is_vendor = False

            try:
                # check if 'items' is in dictionary or else raise error
                data['items'] = json.loads(request.data["items"])
            except:raise ValidationError("items must be in dictionary, eg- {'name':'item name'}")
            
            # data['quantity'] = request.data["quantity"]

            PO_status = request.data["status"]
            PO_status = PO_status.lower()

            if PO_status == "placed" or PO_status == "cancelled" and obj_PO.status == "completed":
                # if PO status is matched with placed or cancelled when status is already completed then do nothing.
                pass
            elif PO_status == "placed" and obj_PO.status != "completed":
                if is_vendor:
                    data['status'] = PO_status
                else:
                    raise ValidationError("Only Vendor can change status to 'placed'.")
            elif PO_status == "cancelled" and obj_PO.status != "completed":
                if not is_vendor:
                    data['status'] = PO_status
                else:
                    raise ValidationError("Only user can cancel Purchase Order.")

                
            if obj_PO.status == "completed" or obj_PO.acknowledgment_date != None:
                if is_vendor:
                    return Response({"response":"","message":"Only User can rate the quality."})
                else:
                    data['quality_rating'] = request.data["quality_rating"]

            serializer = Purchase_OrderSerializer(obj_PO,data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({"response":serializer.data,"message":"Purchase Order updated successfully."},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"response":f"Required field - {str(e)}","message":"ERROR"},status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request,pk, *args, **kwargs):
        """
        Only Admin can delete Purchase Order's record.
        """
        try:
            if self.request.user.is_superuser:
                obj_PO = Purchase_Order.objects.get(id=pk)
                obj_PO.delete()
                
                return Response({"response":"","message":"Purchase Order deleted successfully."},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response":"","message":"You are not Admin."},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"response":str(e),"message":"You are not Admin."},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class Purchase_Order_AcknowledgeView(generics.CreateAPIView):
    """
    Purchase Order Acknowledge API view can retrieve single Purchase Order and only vendor can 
    acknowledge order to be completed.

    Parameters:
        - self : represents the instance of the class.
        - request : object that contains metadata about the request.
        - pk (int): Purchase Order's id.
        - args (tuple): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

    Returns:
        Response: JSON response containing details of the specified Purchase Order(s).

    Raises:
        Exception: If the Purchase Order credentials were not specified.
    """
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_Order_AckSerializer

    def create(self, request,pk, *args, **kwargs):
        """
        Only specific vendor can acknowledge Purchase Order to be as completed.
        """
        try:
            obj_PO = Purchase_Order.objects.get(id=pk)
            vendor = Vendor.objects.get(name = self.request.user)
            if obj_PO.vendor == vendor:
                data = {}
                data['status'] = "completed"
                if obj_PO.acknowledgment_date == None:
                    data['acknowledgment_date'] = datetime.now()

                    serializer = Purchase_OrderSerializer(obj_PO,data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
                    return Response({"response":serializer.data,"message":"Purchase Order acknowledged successfully."},status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"response":"","message":"Purchase Order allready acknowledged."},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response":"","message":"You are not Vendor."},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e: 
            return Response({"response":str(e),"message":"ERROR"},status=status.HTTP_400_BAD_REQUEST)

