import json
import traceback

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from records.models import Product, User, Order


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        allPs = list()
        for p in products:
            pr = dict()
            pr["id"] = str(p.id)
            pr["title"] = p.title
            pr["description"] = p.description
            pr["current_price"] = str(p.current_price)
            pr["old_price"] = str(p.old_price)
            pr["size"] = str(p.size)+" ml"
            pr["ratings"] = str(p.ratings)
            pr["num_ratings"] = str(p.num_ratings)
            pr["image"] = str(p.image.url)
            allPs.append(pr)

        return JsonResponse(allPs, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(View):
    def post(self, request):
        try:
            response = dict()
            user_ = json.loads(request.body)
            user = User()
            user.email = user_['email']
            if User.objects.filter(email=user.email).first() is not None:
                response['response'] = "error"
                response["message"] = "Email Taken"
                return JsonResponse(response)
            user.username = user_['username']
            if User.objects.filter(username=user.username).first() is not None:
                response['response'] = "error"
                response["message"] = "Username Taken"
                return JsonResponse(response)

            user.name = user_['name']
            user.phone = user_['phone']
            user.set_password(user_['password'])
            user.save()
        except:
            tb = traceback.format_exc()
            error = dict()
            error["response"] = "error"
            error["message"] = str(tb)
            return JsonResponse(error)
        response = dict()
        response["response"] = "success"
        response["message"] = "Registration Successful"
        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class LoginUser(View):
    def post(self, request):
        try:
            req = json.loads(request.body)
            email = req["email"]
            password = req["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                res = dict()
                res["response"] = "success"
                res["message"] = "Login Successful"
                return JsonResponse(res)

        except:
            tb = traceback.format_exc()
            error = dict()
            error["response"] = "error"
            error["message"] = str(tb)
            return JsonResponse(error)

        error = dict()
        error["response"] = "error"
        error["message"] = "Wrong Username Or Password"

        return JsonResponse(error)


@method_decorator(csrf_exempt, name="dispatch")
class SaveOrders(View):
    def post(self, request):
        try:
            orders = list()
            order_request = json.loads(request.body)
            user_email = order_request["user"]
            products = order_request["products"]
            for pr in products:
                order = Order()
                order.product_id = int(pr["product_id"])
                order.amount = int(pr["count"])
                order.user = User.objects.filter(email=user_email).first()
                order.then_price = Product.objects.get(pk=order.product_id).current_price
                orders.append(order)
                order.save()
            response = dict()
            response["response"] = "success"
            response["message"] = "Checkout Orders Processed Successfully"
            return JsonResponse(response)

        except:
            tb = traceback.format_exc()
            response = dict()
            response["response"] = "error"
            response["message"] = str(tb)
            return JsonResponse(response)
