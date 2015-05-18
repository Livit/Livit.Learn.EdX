from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import FormView

from labster_backoffice.csv_forms import UploadCsvProductForm, UploadCsvProductGroupForm, \
    UploadCsvVoucherForm, UploadCsvVoucherProductForm, UploadCsvPaymentForm, \
    UploadCsvPaymentProductForm, UploadCsvPaymentStripeForm, UploadCsvLicenseForm

from labster_admin.views import StaffMixin

QUEUED_MESSAGE = "We have queued this task to the background service. You are going to get a notification email soon"

class UploadCsvProduct(StaffMixin, FormView):
    template_name = "product/upload_csv_product.html"
    form_class = UploadCsvProductForm

    def get_success_url(self):
        return reverse('labster-backoffice:product:upload-csv-product')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvProduct, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvProduct, self).form_valid(form)


class UploadCsvProductGroup(StaffMixin, FormView):
    template_name = "product/upload_csv_product_group.html"
    form_class = UploadCsvProductGroupForm

    def get_success_url(self):
        return reverse('labster-backoffice:product:upload-csv-product-group')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvProductGroup, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvProductGroup, self).form_valid(form)


class UploadCsvVoucher(StaffMixin, FormView):
    template_name = "vouchers/upload_csv_voucher.html"
    form_class = UploadCsvVoucherForm

    def get_success_url(self):
        return reverse('labster-backoffice:voucher:upload-csv-voucher')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvVoucher, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvVoucher, self).form_valid(form)


class UploadCsvVoucherProduct(StaffMixin, FormView):
    template_name = "vouchers/upload_csv_voucher.html"
    form_class = UploadCsvVoucherProductForm

    def get_success_url(self):
        return reverse('labster-backoffice:voucher:upload-csv-voucher-product')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvVoucherProduct, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvVoucherProduct, self).form_valid(form)


class UploadCsvPayment(StaffMixin, FormView):
    template_name = "payment/upload_csv_payment.html"
    form_class = UploadCsvPaymentForm

    def get_success_url(self):
        return reverse('labster-backoffice:payment:upload-csv-payment')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvPayment, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvPayment, self).form_valid(form)


class UploadCsvPaymentProduct(StaffMixin, FormView):
    template_name = "payment/upload_csv_payment.html"
    form_class = UploadCsvPaymentProductForm

    def get_success_url(self):
        return reverse('labster-backoffice:payment:upload-csv-payment-product')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvPaymentProduct, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvPaymentProduct, self).form_valid(form)


class UploadCsvPaymentStripe(StaffMixin, FormView):
    template_name = "payment/upload_csv_payment.html"
    form_class = UploadCsvPaymentStripeForm

    def get_success_url(self):
        return reverse('labster-backoffice:payment:upload-csv-payment-product')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvPaymentStripe, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvPaymentStripe, self).form_valid(form)


class UploadCsvLicense(StaffMixin, FormView):
    template_name = "license/upload_csv.html"
    form_class = UploadCsvLicenseForm

    def get_success_url(self):
        return reverse('labster-backoffice:payment:upload-csv-payment-product')

    def get_form_kwargs( self ):
        kwargs = super( UploadCsvLicense, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, QUEUED_MESSAGE)
        return super(UploadCsvLicense, self).form_valid(form)