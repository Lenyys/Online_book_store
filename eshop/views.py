
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import  EmailMessage
from django.db import transaction
from django.shortcuts import render
from django.views import View

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView

from eshop.forms import BookForm, ImageForm, CategoryForm, AuthorForm, AddOrCreateAuthorForm, OrderForm
from eshop.models import Book, Category, Image, Autor, Cart, SelectedProduct, Order

# nezapomenout přepnout na strarou stranku home !!!!!!!
def home(request):
    return render(request, 'home.html')

class BookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['-price']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = get_object_or_404(Category, id=category_id)
        return context


class EBookListView(BookListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        # Přebírá filtraci z BookListView a přidává filtr formátu
        return queryset.filter(type='ebook').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'E-knihy'  # volitelně přidej název sekce
        return context


class AudioBookListView(BookListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type='audiobook').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Audioknihy'
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'eshop/book_detail.html'
    context_object_name = 'book'


class StaffBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'eshop/staff/staff_book_list.html'
    context_object_name = 'books'


class StaffBookDetailView(DetailView):
    model = Book
    template_name = 'eshop/staff/staff_book_detail.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    template_name = 'eshop/staff/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('staff_book_list')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'eshop/staff/book_update.html'
    form_class = BookForm

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or reverse_lazy('staff_book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'eshop/staff/book_delete.html'
    success_url = reverse_lazy('staff_book_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context



class ImageCreateView(CreateView):
    model = Image
    template_name = 'eshop/staff/image_create.html'
    form_class = ImageForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('staff_book_detail', kwargs={'pk':self.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context


class ImageUpdateView(UpdateView):
    model = Image
    template_name = 'eshop/staff/image_update.html'
    form_class = ImageForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('book_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.book
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or reverse_lazy('staff_book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'eshop/staff/image_delete.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or reverse_lazy('staff_book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context



class AddOrCreateAuthorView(FormView):
    template_name = 'eshop/staff/add_or_create_author.html'
    form_class = AddOrCreateAuthorForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        author = form.cleaned_data.get('existing_author')
        if not author:
            author = Autor.objects.create(
                name=form.cleaned_data.get('new_author_name'),
                lastname=form.cleaned_data.get('new_author_lastname'),
                date_of_birth=form.cleaned_data.get('new_author_birthdate', None))

        self.book.autor.add(author)
        return redirect('staff_book_detail', pk=self.book.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context


class AuthorCreateView(CreateView):
    model = Autor
    template_name = 'eshop/staff/author_create.html'
    form_class = AuthorForm
    success_url = reverse_lazy('staff_author_list')

class StaffAuthorDetailView(DetailView):
    model = Autor
    template_name = 'eshop/staff/staff_author_detail.html'
    context_object_name = 'author'

class AuthorUpdateView(UpdateView):
    model = Autor
    template_name = 'eshop/staff/author_update.html'
    form_class = AuthorForm

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or reverse_lazy('staff_author_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context

class StaffAuthorListView(ListView):
    model = Autor
    template_name = 'eshop/staff/staff_author_list.html'
    context_object_name = 'authors'


class AuthorDeleteView(DeleteView):
    model = Autor
    template_name = 'eshop/staff/author_delete.html'
    success_url = reverse_lazy('staff_author_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class RemoveAuthorFromBook(View):
    template_name = 'eshop/staff/remove_author_from_book.html'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['book_id'])
        self.author = get_object_or_404(Autor, pk=kwargs['author_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(f"autor: self.author.name")
        return render(request, self.template_name, {
            'book': self.book,
            'author': self.author,
            'next': request.GET.get('next', reverse('staff_book_detail', kwargs={'pk': self.book.pk}))
        })

    def post(self, request, *args, **kwargs):
        self.book.autor.remove(self.author)
        next_url = request.POST.get('next') or reverse('staff_book_detail', kwargs={'pk': self.book.pk})
        return redirect(next_url)


class CategoryListView(ListView):
    model = Category
    template_name = 'eshop/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'eshop/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'eshop/category_detail.html'
    context_object_name = 'category'


class StaffCategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'eshop/staff/staff_category_list.html'
    context_object_name = 'categories'


class StaffCategoryDetailView(DetailView):
    model = Category
    template_name = 'eshop/staff/staff_category_detail.html'
    context_object_name = 'category'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'eshop/staff/staff_category_confirm_delete.html'  # ← upraveno
    success_url = reverse_lazy('staff_category_list')  # ← možná bylo původně 'category-list'


class StaffCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'eshop/staff/staff_category_form.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('staff_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', reverse('staff_category_list'))
        return context



class CartDetailView(TemplateView):
    template_name = 'eshop/cart_detail.html'

    def get_cart(self):
        request = self.request
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key, user=None).first()
            if not cart:
                cart = Cart.objects.create(session_key=session_key)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        context['cart'] = cart
        context['total_price'] = cart.get_total_cart_price()
        context['items'] = cart.selected_products.all() if cart else []
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)

        cart_item, created = SelectedProduct.objects.get_or_create(cart=cart, product=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart_detail')

class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if key.startswith('quantity-'):
                try:
                    item_id = int(key.split('-')[1])
                    quantity = int(value)
                    if quantity < 1:
                        continue  # nebo item.delete() pokud chceš mazat
                    item = SelectedProduct.objects.get(id=item_id)
                    if item.product.stock_quantity < quantity:
                        item.quantity = item.product.stock_quantity
                        messages.info(request, f"Množství, které jste zadali u knihy {item.product.name} je větší než dostupné množství "
                                               "- zadanou hodnotu jsme upravili na největší možnou")
                    else:
                        item.quantity = quantity
                    item.save()
                except (ValueError, SelectedProduct.DoesNotExist):
                    continue
        return redirect('cart_detail')


class RemoveFromCartView(View):
    def get(self, request, item_id, *args, **kwargs):
        try:
            item = SelectedProduct.objects.get(id=item_id)
            item.delete()
            messages.success(request, "Položka byla odstraněna z košíku.")
        except SelectedProduct.DoesNotExist:
            messages.error(request, "Položka nebyla nalezena.")
        return redirect('cart_detail')


class CreateOrderWithFormView(FormView):
    template_name = 'eshop/order_form.html'
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, is_temporary=True)
        else:
            cart = get_object_or_404(Cart, user=None, session_key=self.request.session.session_key)
        for cart_item in cart.selected_products.all():
            if cart_item.product.stock_quantity < cart_item.quantity:
                messages.warning(request, f"Položka {cart_item.product.name} již není dostupná prosím aktualizujte si nákupní košík")
                return redirect('cart_detail')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        delivery_address = form.cleaned_data.get('delivery_address')
        note = form.cleaned_data.get('note')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        postal_code = form.cleaned_data.get('postal_code')

        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, is_temporary=True)
        else:
            cart = get_object_or_404(Cart, user=None, session_key=self.request.session.session_key)
        with transaction.atomic():
            if self.request.user.is_authenticated:
                order = Order.objects.create(
                    user=self.request.user,
                    delivery_address=delivery_address,
                    total_price=cart.get_total_cart_price(),
                    paid=False,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    postal_code=postal_code,
                    note=note
                )
            else:
                order = Order.objects.create(
                    user=None,
                    delivery_address=delivery_address,
                    total_price=cart.get_total_cart_price(),
                    paid=False,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    postal_code=postal_code,
                    note=note
                )
            for item in cart.selected_products.all():
                # print (f"item.product.stock_quantity {item.product.stock_quantity}")
                # print (f"item.quantity {item.quantity}")
                item.product.stock_quantity -= item.quantity
                item.product.save()
                item.order = order
                # item.cart = None
                item.product_price = item.product.price
                item.save()

            cart.is_temporary = True
            cart.save()

        return redirect('order_detail', pk=order.id)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'eshop/order_detail.html'

class OrderSentView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        email = EmailMessage(
            subject='Potvrzení objednávky',
            body=f'Děkujeme za objednávku... č. {order.id}',
            from_email='eshop@example.com',
            to=[order.email],
        )
        email.send()
        for item in order.selected_products.all():
            item.cart = None
            item.save()
        return redirect('order_confirmation', pk=order_id)

class OrderConfirmationView(TemplateView):
    template_name = 'eshop/order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context


from django.http import HttpResponseForbidden


def delete_category_immediately(request, pk):
    if request.method != 'GET':
        return HttpResponseForbidden("Mazání je povoleno jen přes GET.")

    category = get_object_or_404(Category, pk=pk)
    category_name = category.name
    category.delete()
    messages.success(request, f'Kategorie „{category_name}“ byla úspěšně smazána.')

    next_url = request.GET.get('next')
    return redirect(next_url) if next_url else redirect('category-list')