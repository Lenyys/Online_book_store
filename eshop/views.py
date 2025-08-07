import requests
from datetime import timedelta, datetime, date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView

from eshop.forms import BookForm, ImageForm, CategoryForm, AuthorForm, AddOrCreateAuthorForm, OrderForm #, ImageFormSet
from eshop.mixins import StaffRequiredMixin
from eshop.models import Book, Category, Image, Autor, Cart, SelectedProduct, Order


def home(request):
    books = Book.objects.all()
    ebooks = books.filter(type='ebook')
    books = books.filter(type='book')
    print(f"ebook pocet: {len(ebooks)}")
    time_delta = timezone.now() - timedelta(days=30)
    new_books = books.filter(created_at__gte=time_delta)
    new_ebooks = ebooks.filter(created_at__gte=time_delta)
    print(f"ebook new pocet: {len(new_ebooks)}")
    return render(request, 'home.html', {
        'books': books,
        'new_ebooks': new_ebooks,
        'new_books': new_books,
    })

def search_view(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Book.objects.filter(name__icontains=query)
    return render(request, "eshop/search_results.html", {
        "query": query,
        "results": results
    })


@require_GET
def autocomplete_search(request):
    query = request.GET.get("q", "").strip()
    data = []

    if query:
        qs = Book.objects.filter(name__icontains=query)[:6]
        for book in qs:
            data.append({
                "id": book.pk,
                "name": book.name,
            })

    return JsonResponse({"results": data})


class CategoryListView(ListView):
    model = Category
    template_name = 'eshop/category_list.html'
    context_object_name = 'categories'


class StaffCategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'eshop/staff/staff_category_list.html'
    context_object_name = 'categories'


class StaffCategoryCreateView(PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/staff/staff_category_form.html'
    permission_required = 'eshop.add_category'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('staff_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', reverse('staff_category_list'))
        context['page_title'] = 'Vytvořit kategorii'
        return context


class StaffCategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/staff/staff_category_form.html'
    permission_required = 'eshop.change_category'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('staff_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', reverse('staff_category_list'))
        context['page_title'] = 'Upravit kategorii'
        return context


class StaffCategoryDetailView(DetailView):
    model = Category
    template_name = 'eshop/staff/staff_category_detail.html'
    context_object_name = 'category'


class StaffCategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'eshop/staff/staff_category_confirm_delete.html'
    permission_required = 'eshop.delete_category'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('staff_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', reverse('staff_category_list'))
        return context


class BookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['-price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(type='book')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class EBookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['-price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(type='ebook')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AudioBookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['-price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(type='audiobook')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'eshop/book_detail.html'
    context_object_name = 'book'


class StaffBookListView(StaffRequiredMixin, ListView):
    model = Book
    template_name = 'eshop/staff/staff_book_list.html'
    context_object_name = 'books'


class StaffBookDetailView(StaffRequiredMixin, DetailView):
    model = Book
    template_name = 'eshop/staff/staff_book_detail.html'
    context_object_name = 'book'


class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'eshop/staff/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('staff_book_list')
    permission_required = 'eshop.add_book'


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'eshop/staff/book_update.html'
    form_class = BookForm
    permission_required = 'eshop.change_book'

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return next_url or reverse_lazy('staff_book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'eshop/staff/book_delete.html'
    success_url = reverse_lazy('staff_book_list')
    permission_required = 'eshop.delete_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class FavoriteBooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'eshop/favorite_books.html'
    context_object_name = 'favorite_books'

    def get_queryset(self):
        return self.request.user.favorite_books.all()

class FavoriteBookRemoveFromFavoritesList(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return render(request, 'eshop/remove_favorite.html', {
            'book': book,
        })

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        if user in book.favorite_book.all():
            book.favorite_book.remove(user)

        return redirect(reverse('user_favorite_books'))


class FavoriteBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        user = request.user

        if user in book.favorite_book.all():
            book.favorite_book.remove(user)
        else:
            book.favorite_book.add(user)

        next_url = self.request.POST.get('next', '/')
        return redirect(next_url)

    # def get(self, request, book_id):
    #     book = get_object_or_404(Book, id=book_id)
    #     user = request.user
    #
    #     if user in book.favorite_book.all():
    #         book.favorite_book.remove(user)
    #     else:
    #         book.favorite_book.add(user)
    #
    #     next_url = self.request.GET.get('next', '/')
    #     return redirect(next_url)


class ImageCreateView(PermissionRequiredMixin, CreateView):
    model = Image
    template_name = 'eshop/staff/image_create.html'
    form_class = ImageForm
    permission_required = 'eshop.add_image'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('staff_book_detail', kwargs={'pk': self.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context


class ImageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Image
    template_name = 'eshop/staff/image_update.html'
    form_class = ImageForm
    permission_required = 'eshop.change_image'

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
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    template_name = 'eshop/staff/image_delete.html'
    permission_required = 'eshop.delete_image'

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return next_url or reverse_lazy('staff_book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class AddOrCreateAuthorView(PermissionRequiredMixin, FormView):
    template_name = 'eshop/staff/add_or_create_author.html'
    form_class = AddOrCreateAuthorForm
    permission_required = ['eshop.add_autor', 'eshop.change_book']

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


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Autor
    template_name = 'eshop/staff/author_create.html'
    form_class = AuthorForm
    success_url = reverse_lazy('staff_author_list')
    permission_required = 'eshop.add_autor'


class StaffAuthorDetailView(StaffRequiredMixin, DetailView):
    model = Autor
    template_name = 'eshop/staff/staff_author_detail.html'
    context_object_name = 'author'


class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Autor
    template_name = 'eshop/staff/author_update.html'
    form_class = AuthorForm
    permission_required = 'eshop.change_autor'

    def get_success_url(self):
        next_url = self.request.POST.get('next') # or self.request.GET.get('next')
        return next_url or reverse_lazy('staff_author_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class StaffAuthorListView(StaffRequiredMixin, ListView):
    model = Autor
    template_name = 'eshop/staff/staff_author_list.html'
    context_object_name = 'authors'


class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Autor
    template_name = 'eshop/staff/author_delete.html'
    success_url = reverse_lazy('staff_author_list')
    permission_required = 'eshop.delete_autor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next', '/')
        return context


class RemoveAuthorFromBook(PermissionRequiredMixin, View):
    template_name = 'eshop/staff/remove_author_from_book.html'
    permission_required = 'eshop.change_book'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['book_id'])
        self.author = get_object_or_404(Autor, pk=kwargs['author_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'book': self.book,
            'author': self.author,
            'next': request.GET.get('next', reverse('staff_book_detail', kwargs={'pk': self.book.pk}))
        })

    def post(self, request, *args, **kwargs):
        self.book.autor.remove(self.author)
        next_url = request.POST.get('next') or reverse('staff_book_detail', kwargs={'pk': self.book.pk})
        return redirect(next_url)



@method_decorator(never_cache, name='dispatch')
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
                        continue
                    item = SelectedProduct.objects.get(id=item_id)
                    if item.product.stock_quantity < quantity:
                        item.quantity = item.product.stock_quantity
                        messages.info(request,
                                      f"Množství, které jste zadali u knihy {item.product.name} není dostupné "
                                      "- množství bylo upraveno")
                    else:
                        item.quantity = quantity
                    item.save()
                except (ValueError, SelectedProduct.DoesNotExist):
                    continue
        return redirect('cart_detail')


class RemoveFromCartView(DeleteView):
    model = SelectedProduct
    template_name = 'eshop/remove_from_cart.html'
    success_url = reverse_lazy('cart_detail')
    context_object_name = 'book'


@method_decorator(never_cache, name='dispatch')
class CreateOrderView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, is_temporary=True)
        else:
            cart = get_object_or_404(Cart, user=None, session_key=self.request.session.session_key)
        if not cart.selected_products.exists():
            return redirect('cart_detail')
        for cart_item in cart.selected_products.all():
            if cart_item.product.stock_quantity < cart_item.quantity:
                cart_item.quantity = cart_item.product.stock_quantity
                cart_item.save()
                messages.warning(request,
                                 f"Položka {cart_item.product.name} již není "
                                 f"dostupná v požadovaném množství - došlo k aktualizaci nákupního košíku")
                if not cart_item.quantity:
                    return redirect(reverse('remove_from_cart', kwargs={'item_id': cart_item.id}))

                return redirect('cart_detail')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, is_temporary=True)
        else:
            cart = get_object_or_404(Cart, user=None, session_key=self.request.session.session_key)
        total_price = cart.get_total_cart_price()
        return render(request, 'eshop/order_form.html', {
            'form': form, 'cart': cart, 'total_price': total_price})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, is_temporary=True)
        else:
            cart = get_object_or_404(Cart, user=None, session_key=self.request.session.session_key)
        total_price = cart.get_total_cart_price()
        if form.is_valid():
             with transaction.atomic():
                order = form.save(commit=False)
                if self.request.user.is_authenticated:
                    order.user = self.request.user
                else:
                    order.user = None
                order.total_price = cart.get_total_cart_price()
                order.paid = False
                order.save()
                for item in cart.selected_products.all():
                    item.product.stock_quantity -= item.quantity
                    item.product.save()
                    item.order = order
                    item.cart = None
                    item.product_price = item.product.price
                    item.save()

                cart.is_temporary = True
                cart.save()
                email = EmailMessage(
                    subject='Potvrzení objednávky',
                    body=f'Děkujeme za objednávku... č. {order.id}',
                    from_email='eshop@example.com',
                    to=[order.email],
                )
                email.send()
             return redirect('order_confirmation', pk=order.id)
        return render(request, 'eshop/order_form.html', {
            'form': form, 'cart': cart, 'total_price': total_price })


class OrderConfirmationView(TemplateView):
    template_name = 'eshop/order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context


def delete_category_immediately(request, pk):
    if request.method != 'GET':
        return HttpResponseForbidden("Mazání je povoleno jen přes GET.")

    category = get_object_or_404(Category, pk=pk)
    category_name = category.name
    category.delete()
    messages.success(request, f'Kategorie „{category_name}“ byla úspěšně smazána.')

    next_url = request.GET.get('next')
    return redirect(next_url) if next_url else redirect('category-list')


def exchange_rate_page(request):
    exchange_rates = request.session.get("exchange_rates_cnb")
    today = date.today()
    exchange_valid_for = None
    last_change = request.session.get('exchange_rate_last_change')
    if last_change:
        try:
            last_change = datetime.strptime(last_change, "%Y-%m-%d").date()
        except Exception as e:
            print("Chyba při parsování last_change:", e)
            last_change = None
    if exchange_rates:
        try:
            exchange_valid_for_str = exchange_rates["EUR"][1]
            exchange_valid_for = datetime.strptime(exchange_valid_for_str, "%Y-%m-%d").date()
            # print(f"valid_for: {exchange_valid_for}")
            # print(f"valid_for < today: {exchange_valid_for < today}")
        except Exception as e:
            print("Chyba při parsování validFor:", e)
    if not exchange_rates or (
            exchange_valid_for and exchange_valid_for < today and (
            not last_change or last_change < today)):
        print("stahujeme nový kurzoový lístek z cnb")
        url = "https://api.cnb.cz/cnbapi/exrates/daily"
        params = {}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            currency_wanted = ["EUR", "USD"]
            exchange_rates = {
                rate["currencyCode"]: (rate["rate"], rate["validFor"])
                for rate in data.get("rates", [])
                if rate["currencyCode"] in currency_wanted
            }
            request.session["exchange_rates_cnb"] = exchange_rates
            request.session["exchange_rate_last_change"] = today.isoformat()
            print("uloženo do session")

        except Exception as e:
            print(e)

    exchange_rates_dict = {}
    for currency, (cur_rate, valid_for) in exchange_rates.items():
        exchange_rates_dict[currency] = cur_rate

    return render(request, 'eshop/exchange_rate.html', {
        'exchange_rates_dict': exchange_rates_dict
    })
