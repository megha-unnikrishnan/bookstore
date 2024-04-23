from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.cache import cache_control

from order.models import Order, OrderProduct
from userapp.models import CustomUser
from shop.models import Category,Author,Book,Offer,Bookvariant,MultipleImages,Editions
import os
from cart.models import Coupons
from adminapp.forms import CategoryUpdateform
from datetime import datetime

def admin_login(request):
    try:
        if request.user.is_superuser and request.user.is_authenticated:
            return redirect('admindashboard')
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    request.session['email'] = email
                    return redirect('admindashboard')
                else:
                    messages.info(request, "Invalid credentials")
            else:
                messages.info(request, "Invalid credentials")
                return redirect('adminlogin')

    except Exception as e:
        print(e)
        return redirect('adminlogin')
    return render(request, 'adminview/login.html')




def admin_dashboard(request):
    if 'email' in request.session:

        return render(request, 'adminview/admindashboard.html')
    return redirect('adminlogin')



def admin_logout(request):
    logout(request)
    return redirect('adminlogin')



def admin_users(request):
    if 'email' in request.session:
        user = CustomUser.objects.all()
        context = {'user': user}
        return render(request, 'adminview/admin-users.html', context)
    return redirect('adminlogin')




def admin_action(request, id):
    user = CustomUser.objects.get(id=id)
    print(user)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('users')


@cache_control(no_cache=True, no_store=True)
def admin_category_action(request, id):
    user = Category.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('admincategory')

@cache_control(no_cache=True, no_store=True)
def admin_add_product(request):
    if 'email' in request.session:
        try:
            if request.method=='POST':
                name=request.POST['name']
                image = request.FILES.get('image')
                description = request.POST['description']
                review = request.POST['review']

                book=Book(product_name=name,product_image=image,product_desc=description,review=review)
                print(book)
                book.save()
                messages.success(request,"successfully saved")
                return redirect("adminproduct")

        except Exception as e:
            print(e)
            messages.error(request, "Save Failed")
            return redirect("adminproduct")
        return render(request, 'adminview/admin-add-product.html')
    return redirect('adminlogin')

@cache_control(no_cache=True, no_store=True)
def admin_author_action(request, id):
    user = Author.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('adminauthor')

@cache_control(no_cache=True, no_store=True)
def admin_product_action(request, id):
    user = Book.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('adminproduct')


@cache_control(no_cache=True, no_store=True)
def admin_edit_product(request,id):
    if 'email' in request.session:
        context = {}
        try:
            book = Book.objects.get(id=id)
            context = {'book': book}
            if request.method == "POST":
                if request.FILES:
                    os.remove(book.product_image.path)
                    book.product_image = request.FILES['image']
                book.product_name = request.POST['name']
                book.product_desc = request.POST['description']
                book.review = request.POST['review']
                book.save()
                messages.success(request, "Succesfully updated all details")
                return redirect('adminproduct')
            return render(request, 'adminview/admin-edit-product.html', context)



        except Exception as e:
            print(e)
            messages.error(request, "Saved failed")
            return redirect('admincategory')
    return redirect('adminlogin')

@cache_control(no_cache=True, no_store=True)
def admin_product(request):
    if 'email' in request.session:
        book=Book.objects.all()

        context={
            'book':book
        }
        return render(request,'adminview/adminproduct.html',context)
    return redirect('adminlogin')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='adminlogin')
def admin_add_author(request):
    if 'email' in request.session:
        try:
            if request.method=='POST':
                name=request.POST['name']
                image = request.FILES.get('image')
                description = request.POST['description']

                author=Author(author_name=name,author_image=image,author_desc=description)
                author.save()
                messages.success(request, "Succesfully added")
                return redirect("adminauthor")
        except Exception as e:
            print(e)
            messages.error(request, "Saved failed")
            return redirect("adminauthor")
        return render(request, 'adminview/adminaddauthor.html')
    return redirect('adminlogin')



@cache_control(no_cache=True, no_store=True)
def admin_edit_author(request, id):
    if 'email' in request.session:
        context = {}
        try:
            author = Author.objects.get(id=id)
            context = {'author': author}
            if request.method == "POST":
                print(request.POST)
                if request.FILES:
                    os.remove(author.author_image.path)
                    author.author_image = request.FILES['image']
                author.author_name = request.POST['name']
                author.author_desc = request.POST['description']
                author.save()
                messages.info(request, "Succesfully updated all details")
                return redirect('adminauthor')
            return render(request, 'adminview/admin-author-edit.html', context)



        except Exception as e:
            print(e)
            return redirect('admincategory')
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
def admin_author(request):
    if 'email' in request.session:
        author=Author.objects.all()
        context={
            'author':author
        }
        return render(request,'adminview/adminauthor.html',context)
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
def admin_add_category(request):
    if 'email' in request.session:
        try:
            if request.method=='POST':
                name=request.POST['name']
                image = request.FILES.get('image')
                description = request.POST['description']
                category=Category(category_name=name,category_image=image,category_desc=description)
                category.save()
                messages.error(request, 'Saved Successfully')
                return redirect("admincategory")

        except Exception as e:
            messages.error(request,'Saved failed')
            return redirect("admincategory")
        return render(request, 'adminview/admin-add-category.html')
    return redirect('adminlogin')



@cache_control(no_cache=True, no_store=True)
def admin_category(request):
    if 'email' in request.session:
        category=Category.objects.all()
        context={
            'category':category
        }
        return render(request,'adminview/admincategory.html',context)
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='adminlogin')
def admin_edit_category(request, id):
    if 'email' in request.session:
        context = {}
        print("call fucntion")
        try:
            category = Category.objects.get(id=id)
            print(category)
            print(category.category_name)
            context = {'category': category}
            if request.method == "POST":
                print(request.POST)
                if request.FILES:
                    os.remove(category.category_image.path)
                    category.category_image = request.FILES['catimage']
                category.category_name = request.POST['catname']
                print(category.category_name)
                category.category_desc = request.POST['description']
                category.offer = 12

                category.save()
                print('after save')
                messages.success(request, "Succesfully updated all details")
                return redirect('admincategory')
            return render(request, 'adminview/admin-edit-category.html', context)



        except Exception as e:
            print(e)
            return redirect('admincategory')
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='adminlogin')
def admin_delete_category(request, id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect('admincategory')
# Create your views here.

@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='adminlogin')
def admin_offer_add(request):
    if 'email' in request.session:
        try:
            if request.method=='POST':
                name=request.POST['name']
                percentage = request.POST['percentage']
                startdate = request.POST['startdate']
                enddate = request.POST['enddate']
                offer=Offer(name=name,off_percent=percentage,start_date=startdate,end_date=enddate)
                offer.save()
                messages.success(request, 'Saved successfully')
                return redirect("admincategory")

        except Exception as e:
            print(e)
            messages.error(request,'saved failed')
        return render(request, 'adminview/admin-add-offer.html')
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
def admin_offer(request):
    if 'email' in request.session:
        offer=Offer.objects.all()
        context={
            'offer':offer
        }
        return render(request,'adminview/admin-offer.html',context)
    return redirect('adminlogin')

@cache_control(no_cache=True, no_store=True)
def admin_edit_offer(request,id):
    if 'email' in request.session:
        context={}
        try:
            offer = Offer.objects.get(id=id)
            context = {'offer': offer}
            if request.method == "POST":
                offer.name = request.POST['name']
                offer.off_percent = request.POST['percentage']
                offer.start_date = request.POST['startdate']
                offer.end_date = request.POST['enddate']
                offer.save()
                messages.info(request, "Succesfully updated all details")
                return redirect('adminoffer')
        except Exception as e:
            print(e)
            messages.info(request, "Succesfully updated all details")
        return render(request, 'adminview/admin-edit-offer.html', context)
    return redirect('adminlogin')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='adminlogin')
def add_product_variant(request):
    if 'email' in request.session:
        context = {}

        try:
            product = Book.objects.all().order_by('id')
            author = Author.objects.all().order_by('id')
            offer = Offer.objects.all().order_by('id')
            category = Category.objects.all().order_by('id')
            edition=Editions.objects.all().order_by('id')

            if request.method == "POST":
                product = request.POST.get('product')
                category = request.POST.get('category')
                author = request.POST.get('author')
                offer = request.POST.get('offer')
                edition = request.POST.get('edition')
                price = request.POST.get('price')
                stock = request.POST.get('stock')
                rating = request.POST.get('rating')

                prod_obj = Book.objects.get(id=product)
                cat_obj = Category.objects.get(id=category)
                author_obj = Author.objects.get(id=author)
                offer_obj = Offer.objects.get(id=offer)
                edition_obj=Editions.objects.get(id=edition)
                print(prod_obj.product_name)

                variant_name = f"{prod_obj.product_name} {author_obj.author_name} {edition_obj.edition_name}"


                try:

                    variant = Bookvariant.objects.get(product=prod_obj, author=author_obj,edition=edition_obj)

                    messages.error(request, "Variant already exists")
                except Bookvariant.DoesNotExist:

                    variant = Bookvariant(

                        variant_name=variant_name,
                        product=prod_obj,
                        author=author_obj,
                        category=cat_obj,
                        edition=edition_obj,
                        product_price=price,
                        stock=stock,
                        rating=rating,
                        offer=offer_obj
                    )

                    variant.save()

                    try:
                        multiple_images = request.FILES.getlist('multipleImage', None)
                        if multiple_images:
                            for image in multiple_images:
                                photo = MultipleImages.objects.create(
                                    product=variant,
                                    images=image,
                                )

                    except Exception as e:
                        print(e)
                        messages.info(request, "Image Upload Failed")
                        return redirect('productaddvariant')

                    messages.info(request, "Product variant saved successfully")
                    return redirect('productaddvariant')

            context = {
                'product': product,
                'author': author,
                'offer': offer,
                'category': category,
                'edition':edition
            }

        except Exception as e:
            print(e)
            return redirect('productaddvariant')

        return render(request, 'adminview/admin-add-product-variant.html', context)
    return redirect('adminlogin')


def admin_edition(request):
    if 'email' in request.session:
        edition=Editions.objects.all()
        context={
            'edition':edition
        }
        return render(request,'adminview/admin-edition.html',context)
    return redirect('adminlogin')


def admin_add_edition(request):
    if 'email' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            publisher = request.POST['publisher']
            year = request.POST['year']

            edition = Editions(edition_name=name, edition_desc=description, publisher=publisher,year=year)
            edition.save()
            return redirect("adminedition")
        return render(request, 'adminview/admin-edition-add.html')
    return redirect('adminlogin')

@cache_control(no_cache=True, no_store=True)
def admin_edit_edition(request,id):
    if 'email' in request.session:
        context={}
        try:
            edition = Editions.objects.get(id=id)
            context = {'edition': edition}
            if request.method == "POST":

                edition.edition_name = request.POST['name']
                edition.edition_desc = request.POST['description']
                edition.publisher=request.POST.get('publisher')
                edition.year=request.POST['year']
                edition.save()
                messages.info(request, "Succesfully updated all details")
                return redirect('adminedition')


        except Exception as e:
            print(e)
            messages.info(request, "Succesfully saved")
        return render(request, 'adminview/admin-edition-edit.html', context)
    return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
def admin_edition_action(request, id):
    user = Editions.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('adminedition')


def admin_offer_action(request,id):
    user = Offer.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('adminoffer')


@cache_control(no_cache=True, no_store=True)
def admin_variant(request):
        if 'email' in request.session:
            context = {}
            try:
                variant = Bookvariant.objects.all()
                variant_images = {}

                for image in variant:
                    images = MultipleImages.objects.filter(product=image)
                    variant_images[image.id] = list(images)
                context = {
                    'variant': variant,
                    'variant_images': variant_images
                }
            except Exception as e:
                print(e)

            return render(request, 'adminview/adminvariant.html', context)
        return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
def admin_variant_edition_action(request, id):
    user = Bookvariant.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('adminvariant')

def admin_edit_product_variant(request, id):
    if 'email' in request.session:
        context = {}

        try:
            variant=Bookvariant.objects.get(id=id)
            print(variant.variant_name,'uu')

            product = Book.objects.all().order_by('id')
            author = Author.objects.all().order_by('id')
            offer = Offer.objects.all().order_by('id')
            category = Category.objects.all().order_by('id')
            edition = Editions.objects.all().order_by('id')
            object_image = MultipleImages.objects.filter(product=id)

            if request.method == "POST":
                product = request.POST.get('product')
                category = request.POST.get('category')
                author = request.POST.get('author')
                offer = request.POST.get('offer')
                edition = request.POST.get('edition')
                price = request.POST.get('price')
                stock = request.POST.get('stock')
                rating = request.POST.get('rating')

                prod_obj = Book.objects.get(id=product)
                cat_obj = Category.objects.get(id=category)
                author_obj = Author.objects.get(id=author)
                offer_obj = Offer.objects.get(id=offer)
                edition_obj = Editions.objects.get(id=edition)

                variant.product = prod_obj
                variant.category = cat_obj
                variant.author = author_obj
                variant.offer = offer_obj
                variant.edition = edition_obj
                variant.product_price = price
                variant.stock = stock
                variant.rating = rating

                multiple_images = request.FILES.getlist('multipleImage', None)
                if multiple_images:
                    if object_image:
                        for image in object_image:
                            os.remove(image.images.path)
                            image.delete()
                        for image in multiple_images:
                            img = MultipleImages.objects.create(
                                product=variant,
                                images=image
                            )
                    else:
                        for image in multiple_images:
                            img = MultipleImages.objects.create(
                                product=variant,
                                images=image
                            )
                variant_name = f"{prod_obj.product_name} {author_obj.author_name} {edition_obj.edition_name}"
                variant.variant_name = variant_name
                variant.save()
                messages.success(request, "Edited Successfully")
                return redirect('adminvariant')


            context = {
                'variant': variant,
                'product': product,
                'author': author,
                'offer': offer,
                'category': category,
                'edition': edition,
                'multiple_images': object_image,

            }
        except Exception as e:
            print(e)




        return render(request,'adminview/admin-edit-variant.html',context)
    return redirect('adminlogin')

def delete_image(request, image_id):
    try:

        image = MultipleImages.objects.get(id=image_id)
        variant_id = image.product.id
        image.delete()

        # Redirect back to the same page after deletion
        return redirect('adminvariantedit',id=variant_id)
    except Exception as e:
        # Handle case where image does not exist
        return redirect('adminvariantedit',id=variant_id)



def coupon_list(request):
    if 'email' in request.session:

        try:

            coupons = Coupons.objects.all()
            context = {
                'coupons': coupons,
            }
            return render(request, 'adminview/admin-coupons.html', context)
        except Coupons.DoesNotExist:
            context = {
                'coupons': None,
                'message': 'No coupons found.',
            }
            return render(request, 'adminview/admin-coupons.html', context)
    return redirect('adminlogin')

def add_coupon(request):
    if 'email' in request.session:
        try:
            if request.method == "POST":
                coupon_code = request.POST.get("coupon_code")
                min_amount = request.POST.get("min_amount")
                off_percent = request.POST.get("off_percent")
                max_discount = request.POST.get("max_discount")
                expiry_date = request.POST.get("expiry_date")
                coupon_stock = request.POST.get("coupon_stock")

                # Validate coupon_code
                if coupon_code and coupon_code.islower():
                    messages.warning(request, "Coupon code cannot contain small letters!")
                    return redirect("addcoupon")

                if Coupons.objects.filter(coupon_code=coupon_code).exists():
                    messages.warning(request, "This coupon is already in your account!")
                    return redirect("addcoupon")

                # Validate min_amount
                if not min_amount.isdigit() or int(min_amount) < 500:
                    messages.warning(request, "Minimum amount must be a number greater than or equal to 500!")
                    return redirect("addcoupon")

                # Validate off_percent
                if not off_percent.isdigit() or int(off_percent) <= 0:
                    messages.warning(request, "Off percent must be a positive number greater than 0!")
                    return redirect("addcoupon")

                # Validate max_discount
                if not max_discount.isdigit() or int(max_discount) < int(off_percent):
                    messages.warning(request, "Max discount must be a number greater than or equal to Off percent!")
                    return redirect("addcoupon")

                # Validate expiry_date
                try:
                    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                except ValueError:
                    messages.warning(request, "Invalid expiry date format. Please use YYYY-MM-DD.")
                    return redirect("addcoupon")

                if expiry_date <= timezone.now().date():
                    messages.warning(request, "Expiry date should be in the future!")
                    return redirect("addcoupon")

                # Validate coupon_stock
                if coupon_stock:
                    try:
                        coupon_stock = int(coupon_stock)
                        if coupon_stock < 0:
                            raise ValueError
                    except ValueError:
                        messages.warning(request, "Coupon stock must be a non-negative integer!")
                        return redirect("addcoupon")
                else:
                    coupon_stock = None

                coupon = Coupons(
                    coupon_code=coupon_code,
                    min_amount=min_amount,
                    off_percent=off_percent,
                    max_discount=max_discount,
                    expiry_date=expiry_date,
                    coupon_stock=coupon_stock
                )
                coupon.save()

                messages.success(request, f"{coupon_code} added successfully!")
                return redirect("coupon")

        except Exception as e:
            print(e)
            messages.error(request, "Failed to save coupon!")
            return redirect("addcoupon")

        return render(request, "adminview/admin-add-coupon.html")
    return redirect('adminlogin')


def admin_coupon_action(request, id):
    user = Coupons.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect('coupon')


def admin_edit_coupon(request, id):
    try:
        coupon = Coupons.objects.get(id=id)
        if request.method == "POST":
            coupon_code = request.POST.get("coupon_code")
            min_amount = request.POST.get("min_amount")
            off_percent = request.POST.get("off_percent")
            max_discount = request.POST.get("max_discount")
            expiry_date = request.POST.get("expiry_date")
            coupon_stock = request.POST.get("coupon_stock")

            # Check if the edited coupon code is unique
            if Coupons.objects.exclude(id=id).filter(coupon_code=coupon_code).exists():
                messages.error(request, 'Coupon code must be unique.')
                return redirect('couponedit', id=id)

            # Update the coupon
            Coupons.objects.filter(id=id).update(
                coupon_code=coupon_code,
                min_amount=min_amount,
                off_percent=off_percent,
                max_discount=max_discount,
                expiry_date=expiry_date,
                coupon_stock=coupon_stock
            )
            messages.success(request, f'{coupon_code} updated successfully.')
            return redirect('coupon')

        context = {
            'coupon': coupon
        }
        return render(request, 'adminview/admin-edit-coupon.html', context)
    except Coupons.DoesNotExist:
        messages.error(request, 'Coupon does not exist.')
        return redirect('coupon')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('coupon')


def admin_orders(request):
    if 'email' in request.session:
        context = {}
        try:
            orders = Order.objects.all().order_by('-order_id')
            context = {
                'orders': orders,
            }
        except Exception as e:
            print(e)
        return render(request, 'adminview/admin-order.html', context)
    return redirect('adminlogin')





def admin_order_update(request, id):
    if 'email' in request.session:
        context = {}
        try:
            order = Order.objects.get(id=id)
            order_items = OrderProduct.objects.filter(order_id=id)
            payment = order.payment
            if request.method == 'POST':
                order_status = request.POST.get('orderStatus', None)
                if order_status:
                    order.status = order_status
                    order.save()
                if order_status == 'Delivered':
                    payment.is_paid = True
                payment.save()
                messages.success(request, 'Status updated')
                return redirect('order_update', id)
            context = {
                'order': order,
                'order_items': order_items,
            }
            return render(request, 'adminview/admin_order_update.html', context)
        except Exception as e:
            print(e)
            return redirect('adminorder')
    return redirect('adminlogin')