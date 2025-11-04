# from odoo import http
# from odoo.http import request
# import json
# import logging

# _logger = logging.getLogger(__name__)


# class ApiModuleController(http.Controller):

#     @http.route("/api_module/sync_contacts", type="json", auth="user", methods=["POST"])
#     def sync_contacts(self, config_id=None):
#         """API endpoint to manually trigger contact sync"""
#         try:
#             if config_id:
#                 config = request.env["api.config"].browse(config_id)
#                 if not config.exists():
#                     return {"success": False, "message": "Configuration not found"}
#             else:
#                 # Get the first active configuration
#                 config = request.env["api.config"].search(
#                     [("active", "=", True)], limit=1
#                 )
#                 if not config:
#                     return {
#                         "success": False,
#                         "message": "No active configuration found",
#                     }

#             result = config.sync_contacts_from_odoo()
#             return result

#         except Exception as e:
#             _logger.error(f"Contact sync API error: {str(e)}")
#             return {"success": False, "message": str(e), "errors": [str(e)]}

#     @http.route("/api_module/sync_products", type="json", auth="user", methods=["POST"])
#     def sync_products(self, config_id=None):
#         """API endpoint to manually trigger product sync"""
#         try:
#             if config_id:
#                 config = request.env["api.config"].browse(config_id)
#                 if not config.exists():
#                     return {"success": False, "message": "Configuration not found"}
#             else:
#                 # Get the first active configuration
#                 config = request.env["api.config"].search(
#                     [("active", "=", True)], limit=1
#                 )
#                 if not config:
#                     return {
#                         "success": False,
#                         "message": "No active configuration found",
#                     }

#             result = config.sync_products_from_odoo()
#             return result

#         except Exception as e:
#             _logger.error(f"Product sync API error: {str(e)}")
#             return {"success": False, "message": str(e), "errors": [str(e)]}

#     @http.route("/api_module/sync_all", type="json", auth="user", methods=["POST"])
#     def sync_all(self, config_id=None):
#         """API endpoint to manually trigger all sync operations"""
#         try:
#             if config_id:
#                 config = request.env["api.config"].browse(config_id)
#                 if not config.exists():
#                     return {"success": False, "message": "Configuration not found"}
#             else:
#                 # Get the first active configuration
#                 config = request.env["api.config"].search(
#                     [("active", "=", True)], limit=1
#                 )
#                 if not config:
#                     return {
#                         "success": False,
#                         "message": "No active configuration found",
#                     }

#             results = config.sync_all_data()
#             return {
#                 "success": True,
#                 "message": "All sync operations completed",
#                 "results": results,
#             }

#         except Exception as e:
#             _logger.error(f"All sync API error: {str(e)}")
#             return {"success": False, "message": str(e), "errors": [str(e)]}

#     @http.route(
#         "/api_module/test_connection", type="json", auth="user", methods=["POST"]
#     )
#     def test_connection(self, config_id=None):
#         """API endpoint to test API connection"""
#         try:
#             if config_id:
#                 config = request.env["api.config"].browse(config_id)
#                 if not config.exists():
#                     return {"success": False, "message": "Configuration not found"}
#             else:
#                 # Get the first active configuration
#                 config = request.env["api.config"].search(
#                     [("active", "=", True)], limit=1
#                 )
#                 if not config:
#                     return {
#                         "success": False,
#                         "message": "No active configuration found",
#                     }

#             # Test authentication
#             if config.authenticate():
#                 return {
#                     "success": True,
#                     "message": "Connection successful",
#                     "token": config.token,
#                 }
#             else:
#                 return {"success": False, "message": "Authentication failed"}

#         except Exception as e:
#             _logger.error(f"Connection test error: {str(e)}")
#             return {"success": False, "message": str(e)}

#     @http.route("/api_module/job_history", type="json", auth="user", methods=["POST"])
#     def get_job_history(self, config_id=None, limit=10):
#         """API endpoint to get sync job history"""
#         try:
#             domain = []
#             if config_id:
#                 domain.append(("config_id", "=", config_id))

#             jobs = request.env["sync.job"].search(
#                 domain, limit=limit, order="create_date desc"
#             )

#             job_data = []
#             for job in jobs:
#                 job_data.append(
#                     {
#                         "id": job.id,
#                         "config_name": job.config_id.name,
#                         "job_type": job.job_type,
#                         "status": job.status,
#                         "message": job.message,
#                         "records_processed": job.records_processed,
#                         "errors": job.errors,
#                         "create_date": (
#                             job.create_date.isoformat() if job.create_date else None
#                         ),
#                         "complete_date": (
#                             job.complete_date.isoformat() if job.complete_date else None
#                         ),
#                     }
#                 )

#             return {"success": True, "jobs": job_data, "total": len(job_data)}

#         except Exception as e:
#             _logger.error(f"Job history API error: {str(e)}")
#             return {"success": False, "message": str(e)}

#     @http.route("/api_module/configurations", type="json", auth="user", methods=["GET"])
#     def get_configurations(self):
#         """API endpoint to get all configurations"""
#         try:
#             configs = request.env["api.config"].search([])

#             config_data = []
#             for config in configs:
#                 config_data.append(
#                     {
#                         "id": config.id,
#                         "name": config.name,
#                         "api_url": config.api_url,
#                         "active": config.active,
#                         "sync_contacts": config.sync_contacts,
#                         "sync_products": config.sync_products,
#                         "sync_interval": config.sync_interval,
#                         "last_sync_date": (
#                             config.last_sync_date.isoformat()
#                             if config.last_sync_date
#                             else None
#                         ),
#                     }
#                 )

#             return {
#                 "success": True,
#                 "configurations": config_data,
#                 "total": len(config_data),
#             }

#         except Exception as e:
#             _logger.error(f"Configurations API error: {str(e)}")
#             return {"success": False, "message": str(e)}
