from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Category
from .models import Product

# Create your views here.

# Product view
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = self.object.categories.all()  # tất cả category của product
        return context

# Product Pagination view
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.prefetch_related('categories')

# Product Filter(Category - Price) + Pagination
class ProductFilterView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/filter.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('categories')
        # Lấy giá trị từ query parameters (URL)
        category_id = self.request.GET.get('category', '')
        min_price = self.request.GET.get('minPrice', '')
        max_price = self.request.GET.get('maxPrice', '')

        # Lọc theo category nếu có
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # Lọc theo min_price nếu có
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        # Lọc theo max_price nếu có
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()  # tránh duplicate nếu nhiều category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Truyền lại các giá trị filter để giữ trong form template
        context['selected_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('minPrice', '')
        context['max_price'] = self.request.GET.get('maxPrice', '')
        return context


# Product Search + Pagination
class ProductSearchView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/search.html'
    paginate_by = 10
    def get_queryset(self):
        queryset = Product.objects.prefetch_related('categories')
        category_id = self.request.GET.get('category', '')
        keyword = self.request.GET.get('keyword', '')

        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Truyền lại các giá trị filter để giữ trong form template
        context['selected_category'] = self.request.GET.get('category', '')
        context['keyword'] = self.request.GET.get('keyword', '')
        return context
