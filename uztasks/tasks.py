from locust import task

from uztasks import UzTaskSet


class SalesTasks(UzTaskSet):
    @task
    def list_sales_orders(self):
        """Request the sales order listing."""
        response = self.client.get(
            '/?controller=sorders&module=sales_order&action=index')
        self.request_resources(response)


class PurchasingTasks(UzTaskSet):
    @task
    def list_sales_orders(self):
        """Request the purchase order listing."""
        response = self.client.get(
            '/?&controller=porders&module=purchase_order&action=index')
        self.request_resources(response)
