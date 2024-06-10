from datetime import datetime

from odoo import http
from odoo.http import request


class ResourceReservationController(http.Controller):
    @http.route('/reserve/new_resource', auth='user', website=True)
    def show_new_reservation_form(self, **kwargs):
        try:
            tags = request.env['resource.reservation.tag'].sudo().search([])
            return request.render("resource_reservation.new_reservation_form", {'tags': tags})
        except Exception as e:
            return request.render("resource_reservation.error_template", {'error': str(e)})

    @http.route('/reserve/new_resource/submit', auth='user', website=True, type='http', methods=['POST'])
    def submit_new_reservation(self, **post):
        try:
            resource_id = int(post.get('resource_name'))
            resource_type_id = int(post.get('resource_type'))
            tag_ids = request.httprequest.form.getlist('reservation_tag_id')
            tag_ids = [int(tid) for tid in tag_ids]
            repeat_type = post.get('repeat')
            repeat_until = post.get('repeat_until')
            start_datetime = post.get('start_datetime').replace('T', ' ')
            end_datetime = post.get('end_datetime').replace('T', ' ')

            # Convert times to datetime objects
            start_datetime = datetime.strptime(start_datetime + ':00', '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(end_datetime + ':00', '%Y-%m-%d %H:%M:%S')
            if repeat_until:
                repeat_until = datetime.strptime(repeat_until.replace('T', ' ') + ':00', '%Y-%m-%d %H:%M:%S')

            reservation_vals = {
                'title': post.get('title'),
                'resource_name': resource_id,
                'resource_type': resource_type_id,
                'reservation_tag_id': [(6, 0, tag_ids)],
                'start_datetime': start_datetime,
                'end_datetime': end_datetime,
                'resource_description': post.get('resource_description'),
                'repeat': repeat_type,
                'repeat_until': repeat_until if repeat_until else False,
                'current_user': request.env.uid,
            }
            new_reservation = request.env['resource.reservation'].sudo().create(reservation_vals)
            return request.redirect('/thank_you')
        except Exception as e:
            request.env.cr.rollback()
            return request.render("resource_reservation.error_template", {'error': str(e)})

    @http.route('/thank_you', auth='public', website=True, type='http')
    def thank_you(self, **kwargs):
        return request.render("resource_reservation.thank_you_template_reservation", {})

