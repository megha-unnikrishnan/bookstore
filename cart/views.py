import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cart.models import CartItem, Cart,Coupons
from shop.models import Bookvariant
from django.shortcuts import redirect
from django.contrib import messages
from userapp.models import CustomUser, UserAddress
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import Order, Payments, OrderProduct
import pdb



# def show_cart(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user, cart__isnull=False)
#     context = {'cart_items': cart_items}
#     return render(request, 'userview/cart.html', context)


def add_to_cart(request, id):
    try:
        if  'email' not in request.session:
            messages.error(request, 'You need to login for add to cart!')
            return redirect('login')
        else:
            product = Bookvariant.objects.get(id=id)
            if product.stock < 0:
                messages.error(request, 'This book is out of stock!!!')
                return redirect('productdetail', id=id)

            user = request.user
            user_obj = CustomUser.objects.get(id=user.id)

            userexists = CartItem.objects.filter(user=user_obj)

            if not userexists.exists():
                token = str(uuid.uuid4())
                cart_obj = Cart(cart_id=token)
                cart_obj.save()
                cart_item = CartItem(user=user_obj, product=product, cart=cart_obj)
                cart_item.save()
                messages.success(request, 'Successfully add to cart!')
                cartitem = CartItem.objects.filter(user=user_obj).count()
                request.session['cart'] = cartitem
                return redirect('productdetail', id=id)


            if userexists.exists():
                productexits = CartItem.objects.filter(Q(product=product)&Q(user=user_obj))
                if productexits.exists():
                    add_product=CartItem.objects.get(Q(product=product)&Q(user=user_obj))
                    print(add_product)
                    if add_product.product.max_quantity_per_person<=add_product.quantity:
                        print("maxcount",add_product.product.max_quantity_per_person)
                        print()
                        messages.error(request,f'user cannot add more than {add_product.product.max_quantity_per_person}')

                        return redirect('productdetail', id=id)
                    elif add_product.product.stock<=add_product.quantity:
                        print(add_product.product.stock)
                        print(add_product.stock)
                        messages.error(request,'item stock exhausted')
                        return redirect('productdetail', id=id)
                    else:
                        add_product.quantity=add_product.quantity+1
                        add_product.save()
                    messages.success(request, 'Successfully add to cart!')
                    return redirect('productdetail', id=id)

                cart_obj = userexists.first().cart
                cartitem = CartItem(user=user_obj, product=product, cart=cart_obj)

                cartitem.save()

                user_id = CustomUser.objects.get(id=request.user.id)
                cartitem = CartItem.objects.filter(user=user_id).count()
                request.session['cart'] = cartitem
                return redirect('productdetail', id=id)

    except Exception as e:
        print(e)
        messages.error(request, 'Add to cart failed')
        return redirect('productdetail', id=id)


def cart_items(request, id):
    context = {}
    try:
        if not 'email' in request.session:
            messages.error(request, 'You need to login for add to cart!')
            return redirect('login')
        else:
            userid = CustomUser.objects.get(id=id)
            cartitem = CartItem.objects.filter(user=userid)
            if cartitem:
                coupon=Coupons.objects.all()
                print(coupon)
            else:
                messages.error(request,'You have not added any items to cart!')
                user_id = CustomUser.objects.get(id=request.user.id)
                cartitem = CartItem.objects.filter(user=user_id).count()
                print('count',cartitem)
                request.session['cart'] = cartitem
                return redirect('userindex')


            # total = sum(item.product.discounted_price() * item.quantity for item in cartitem)
            # withoutoffertotal = sum(item.product.product_price * item.quantity for item in cartitem)
            # offer = withoutoffertotal - total
            # shipping_cost = 90 if withoutoffertotal < 6000 else 0
            # grand_total = withoutoffertotal + offer + shipping_cost


            context = {
                'items': cartitem,
                'coupon':coupon
                # 'total':withoutoffertotal,
                # 'offer':offer,
                # 'grand_total':grand_total


            }
    except Exception as e:
        print(e)

    return render(request, 'userview/cart.html', context)


def delete_cart_item(request, id):
    try:
        if not 'email' in request.session:
            messages.error(request, 'You need to login for add to cart!')
            return redirect('login')
        try:
            cart_item = get_object_or_404(CartItem, id=id, user=request.user)
            cart_item.delete()

            messages.success(request, "Cart item deleted successfully")
            user_id = CustomUser.objects.get(id=request.user.id)
            cartitem = CartItem.objects.filter(user=user_id).count()
            request.session['cart'] = cartitem
            return redirect('cart', id=request.user.id)
        except CartItem.DoesNotExist:
            messages.error(request, "Cart item does not exist")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('cart', id=request.user.id)
    except Exception as e:
        print(e)


@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        item_id_str = request.POST.get('item_id')
        coupon_code = request.POST.get('coupon_code')
        new_quantity_str = request.POST.get('new_quantity')
        print(coupon_code)
        try:
            new_quantity = int(new_quantity_str) if new_quantity_str.isdigit() else 0
        except ValueError:
            new_quantity = 0
            # Retrieve the cart item

        if item_id_str.isdigit():
            item_id = int(item_id_str)

            cart_item = CartItem.objects.get(id=item_id)

        else:

            user = CustomUser.objects.get(id=request.user.id)
            cart_item = CartItem.objects.filter(user=user)

        print('2')
        print(item_id_str)
        if item_id_str.isdigit():
            item_id = int(item_id_str)

            cart_item = CartItem.objects.get(id=item_id)

        else:
            print("else")
            user_id = CustomUser.objects.get(id=request.user.id)
            print(user_id)
            cart_item = CartItem.objects.filter(user=user_id).first()



        print('3')

        if new_quantity != 0:
            cart_item.quantity = new_quantity
            if cart_item.product.max_quantity_per_person < cart_item.quantity:
                return JsonResponse(
                    {'error': f'User cannot add more than {cart_item.product.max_quantity_per_person} quantity to the cart!!',
                     'hide_quantity': True})
            cart_item.save()

        if cart_item.product.stock < new_quantity:
            return JsonResponse({'error': 'Exceeded available stock', 'hide_quantity': True})


        if new_quantity != 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        # Calculate new subtotal and grand total
        print('4')
        print(new_quantity)
        if new_quantity != 0:
            sub_total = int(cart_item.product.discounted_price()) * new_quantity
            print(sub_total)
        else:
            sub_total = int(cart_item.product.discounted_price()) * cart_item.quantity
        # subtotal = int(cart_item.product.discounted_price()) * new_quantity
        if new_quantity != 0:
            offerpricetotal = int(cart_item.product.product_price) * new_quantity
            print(offerpricetotal)
        else:
            offerpricetotal = int(cart_item.product.product_price) * cart_item.quantity

        print(offerpricetotal)
        print('5')
        user_id = CustomUser.objects.get(id=request.user.id)
        cartitem = CartItem.objects.filter(user=user_id)


        total = sum(item.product.discounted_price() * item.quantity for item in cartitem)

        withoutoffertotal = sum(item.product.product_price * item.quantity for item in cartitem)
        print(withoutoffertotal)

        offer = withoutoffertotal - total
        print('offer',offer)

        shipping_cost = 0
        if total < 7000:
            shipping_cost = 90
        else:
            shipping_cost = 0
        try:
            get_coupon = Coupons.objects.get(coupon_code=coupon_code)
        except Coupons.DoesNotExist:
            get_coupon = None
        discount_amount = 0
        message=''
        user_id = CustomUser.objects.get(id=request.user.id)
        cart_item = CartItem.objects.filter(user=user_id).first()
        cart_obj = Cart.objects.get(id=cart_item.cart.id)
        if cart_obj.coupon:
            message=f'Applied coupon code{cart_obj.coupon.coupon_code} successfully'

            discount_amount = total * int(cart_obj.coupon.off_percent) / 100
            print('discount', discount_amount)

            if discount_amount > cart_obj.coupon.max_discount:
                discount_amount = cart_obj.coupon.max_discount

        if get_coupon:

            cart_obj.coupon = get_coupon


            if cart_obj.coupon.min_amount>total:
                return  JsonResponse('error',f"amount should be greater than {get_coupon.min_amount}")
            discount_amount = total * int(get_coupon.off_percent) / 100
            if discount_amount > get_coupon.max_discount:
                discount_amount = get_coupon.max_discount




            if get_coupon.min_amount > withoutoffertotal:
                return JsonResponse({'error': f'Amount should be greater than {get_coupon.min_amount}'})

            discount_amount = total * int(get_coupon.off_percent) / 100
            print('discount', discount_amount)

            if discount_amount > get_coupon.max_discount:
                discount_amount = get_coupon.max_discount
            # message = get_coupon.coupon_code
            message=f'Applied coupon code{get_coupon.coupon_code} successfully'
            cart_obj.save()

        user_id = CustomUser.objects.get(id=request.user.id)
        cart_item = CartItem.objects.filter(user=user_id).first()
        cart_obj = Cart.objects.get(id=cart_item.cart.id)

        tax = (withoutoffertotal * 3) // 100
        cart_obj.tax=tax
        cart_obj.save()



        grand_total = withoutoffertotal - offer-discount_amount +tax+ shipping_cost



        return JsonResponse(
            {'subtotal': sub_total, 'total': withoutoffertotal, 'offer': offer, 'shipping': shipping_cost,
             'grand_total': grand_total,'coupon_offer':discount_amount,'tax':tax,'message':message})


def checkout(request):
    try:
        if not 'email' in request.session:
            messages.error(request, 'You need to login for add to cart!')
            return redirect('login')
        user=request.user
        address=UserAddress.objects.filter(user=user)
        address_id = request.GET.get('address_id')
        selected_address = None
        if address_id:
            selected_address = UserAddress.objects.get(pk=address_id)
        context={
            'address':address
        }

    except Exception as e:
        print(e)
    return render(request, 'userview/checkout.html', context)


def checkout_view(request, id):
    try:
        if 'email' not in request.session:
            messages.error(request, 'You need to log in to add items to the cart.')

        address = UserAddress.objects.get(id=id)
        print(address)
        user = CustomUser.objects.get(id=request.user.id)
        print(user)
        cart_items = CartItem.objects.filter(user=user)
        print(cart_items)
        cart_obj_first= CartItem.objects.filter(user=user).first()
        print(cart_obj_first)
        cart_obj = Cart.objects.get(id=cart_obj_first.cart.id)
        print(
            cart_obj
        )
        if cart_obj.coupon:
            coupon_obj=Coupons.objects.get(id=cart_obj.coupon.id)
        else:
            coupon_obj = None

        print(user)
        print(cart_items)
        shipping_cost=0
        discount_amount=0
        discount=0
        tax=0
        mrp=0
        offerprice=0

        for  i in cart_items:
            mrp=mrp+int(i.product.product_price)*i.quantity
            offerprice=offerprice+int(i.product.discounted_price())*i.quantity
            discount=mrp-offerprice

        if cart_obj.coupon:
            discount_amount = offerprice * int(cart_obj.coupon.off_percent) / 100
            if offerprice < cart_obj.coupon.min_amount:
                messages.error(request, f'Minimum amount should be Rs.{cart_obj.coupon.min_amount}')
                return redirect('checkoutview')
            if cart_obj.coupon.max_discount <= discount_amount:
                discount_amount = cart_obj.coupon.max_discount
            if discount_amount > 0:
                offerprice = offerprice - discount_amount


        tax=cart_obj.tax
        if tax>0:
            offerprice=offerprice+tax
        if offerprice < 3000:
            shipping_cost = 150
            offerprice = offerprice + shipping_cost


        grand_total = mrp-discount-discount_amount+tax+shipping_cost

        if request.method == 'POST':

            order = Order()
            order.user = user
            order.address = address
            order.subtotal=mrp
            order.order_total = grand_total  # total amount including tax
            order.discount_amount = discount
            order.tax = tax
            order.is_ordered = True
            order.coupon = coupon_obj
            order.coupon_mount=discount_amount
            order.shipping=shipping_cost
            paymentmethod=request.POST['payment']
            order.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_id = current_date + str(order.id)  # creating order id
            order.order_id = order_id

            order.save()


            payment = Payments.objects.create(
                user=user,
                total_amount=offerprice,
                is_paid=False,
            )


            for item in cart_items:
                prod_obj = Bookvariant.objects.get(id=item.product.id)
                order_item = OrderProduct.objects.create(
                    user=user,
                    order_id=order,
                    payment_id=payment.id,
                    product=prod_obj,
                    quantity=item.quantity,
                    product_price=item.product.product_price,
                    ordered=True,
                )
                prod_obj.stock = prod_obj.stock - item.quantity
                prod_obj.save()
                item.delete()
            try:
                cart_items.delete()
            except:
                pass

            if paymentmethod == 'cod':
                payment.payment_method = 'Cash on delivery'  # set current payment method
                payment_id = order_id + "COD"
                payment.payment_id = payment_id
                payment.save()
                order.payment = payment
                order.save()
                user_id = CustomUser.objects.get(id=request.user.id)
                cartitem = CartItem.objects.filter(user=user_id).count()
                request.session['cart'] = cartitem
                messages.success(request,"ordered successfully")
                return render(request, 'products/confirm-order.html')


        context = {
            'address': address,
            'cart_items': cart_items,
            'mrp': mrp,
            'discount':discount,
            'tax':tax,
            'shipping':shipping_cost,
            'coupon':discount_amount,
            'grand_total':grand_total

        }
        return render(request, 'userview/placeorder.html', context)

    except UserAddress.DoesNotExist:
        messages.error(request, 'Address does not exist.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
    except Exception as e:
        print(e)  # Log the error for debugging
        messages.error(request, 'An error occurred during checkout. Please try again later.')

    return render(request, 'userview/placeorder.html')


def suggest_page_view(request):
    query = request.GET.get('q')
    if query:
        suggestions_queryset = Bookvariant.objects.filter(
            Q(product_name__icontains=query) | Q(category__category_name__icontains=query)
        ).values('product_name', 'category__category_name')
        suggestions = list(suggestions_queryset)

    return render(request, 'userview/search.html', {'suggestions': suggestions, 'query': query})