from django.urls import reverse
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Label(models.Model):
    label_name = models.CharField(max_length=20,
                            db_index=True)
    slug = models.SlugField(max_length=20,
                            unique=True)
    class Meta:
        ordering = ('label_name',)
        verbose_name = 'label'
        verbose_name_plural = 'labels'

    def __str__(self):
        return self.label_name

QUALITY_CHECKING = (
    ('yes', 'YES'),
    ('no', 'NO')
)

class Specification(models.Model):
    spec_name = models.CharField(blank=True, max_length=50)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    depth = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    quality_checking = models.CharField(choices=QUALITY_CHECKING, max_length=3)
    freshness_duration = models.FloatField(blank=True, null=True)
    when_packeting = models.CharField(max_length=50)
    each_box_contains = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ('width',)
        verbose_name = 'specification'
        verbose_name_plural = 'specifications'

    def __str__(self):
        return self.spec_name

AVAILIBILITY = (
    ('In Stock', 'In Stock'),
    ('Out Of Stock', 'Out of Stock')
)


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    feature = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.CharField(choices=AVAILIBILITY, max_length=12)




    class Meta:
        ordering = ('created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:single-product',
                       args=[self.id, self.slug])

    # def get_available_item(self):
    #     if self.available=True:
    #         return message
