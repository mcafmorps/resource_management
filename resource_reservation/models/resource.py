"""Its just show what moduls are imported"""
from odoo import models, fields, api


class Resource(models.Model):
    """ This module create data for Resource fields in odoo
        model resource_reservation"""
    _name = 'resource'
    _description = 'Resource'

    name = fields.Char(string='Resource name', required=True)
    resource_type = fields.Many2one(
        'resource.type',
        string="Resource Type ", required=True)
    resource_capacity = fields.Float(string=" Resource Capacity ",
                                     required=True)
    resource_capacity_text = fields.Char(string=" Resource Capacity  ",
                                         required=True)
    resource_owner = fields.Many2one('res.users', string='Resource owner',
                                     required=True,
                                     options={'no_create': True},
                                     domain=lambda self: [('groups_id', 'in',
                                                           [self.env.ref("resource_reservation."
                                                                         "group_resource_reservation_approver").id])],
                                     default=lambda self: self.env.ref
                                     ("resource_reservation."
                                      "group_resource_reservation_approver")
                                     .users.ids, )
    image = fields.Binary(string='')
    reservation_ids = fields.One2many('resource.reservation',
                                      'resource_name',
                                      string='Reservations')
    confirmed_reservations = fields.One2many('resource.reservation',
                                             'resource_name',
                                             compute='_compute_confirmed')
    cancelled_reservations = fields.One2many('resource.reservation',
                                             'resource_name',
                                             compute='_compute_cancelled')
    resource_tags = fields.Many2many('resource.tag',
                                     string='Resource Tags ',
                                     help="Select one or more resource tags",
                                     widget='many2many_tags')

    @api.depends('reservation_ids')
    def _compute_confirmed(self):
        for record in self:
            record.confirmed_reservations = record.reservation_ids.filtered(
                lambda r: r.booking_status == 'confirmed')

    @api.depends('reservation_ids')
    def _compute_cancelled(self):
        for record in self:
            record.cancelled_reservations = record.reservation_ids.filtered(
                lambda r: r.booking_status == 'cancelled')

    @api.onchange('resource_capacity')
    def _onchange_resource_capacity(self):
        for record in self:
            record.resource_capacity_text = str(record.resource_capacity)


class ResourceType(models.Model):
    _name = 'resource.type'
    _description = 'Resource Type'

    name = fields.Char(string='Resource Type', required=True)
    color_resource_type = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_resource_type', 'UNIQUE (name)',
         'A resource type with the same name already exists.'),
    ]


class ResourceTag(models.Model):
    _name = 'resource.tag'
    _description = 'Resource Tag'

    name = fields.Char(string='Resource Tag', required=True)

    _sql_constraints = [
        ('unique_resource_tag', 'UNIQUE (name)',
         'A resource type with the same name already exists.'),
    ]
