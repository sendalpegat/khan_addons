# -*- coding: utf-8 -*-

from eagle import api, fields, models, _
import datetime

class PersonalDetails(models.Model):
    _inherit = 'res.partner'
    _description = "force member's personal Details for ribbon, medal, cap, belt, ranks etc"
    is_force=fields.Boolean("Is a Force",default=False , translate=True)
    force_id = fields.Many2one("ribbon.medal.force","Force")
    id_no=fields.Char("ID No")
    rank = fields.Many2one("ribbon.medal.rank","Rank",translate=True)
    unit=fields.Many2one("ribbon.medal.force.unit",string="Unit",translate=True ,domain="[('force_name','=',force_id)]")
    post=fields.Many2one("ribbon.medal.post",string="Post",translate=True)
    joining=fields.Date("Joining Date")
    bcs=fields.Boolean("BCS ?")
    retired=fields.Date("Retiered Date")
    service_year=fields.Integer("Service Year")
    service_month=fields.Integer("Service Month")
    service_day=fields.Integer("Service Day")
    service_length=fields.Char("Service Length",compute="calculate_service_length")
    cap=fields.Char("Cap")
    belt=fields.Char("Belt")
    name_tag_eng=fields.Char("Name Tag")
    name_tag_bn=fields.Char("নাম ফলক")
    note=fields.Char("note")
    conf_note=fields.Char("confidential")
    freedom_f=fields.Boolean("Freedom Fighter")
    nirapotta=fields.Boolean("Nirapotta")
    bpa=fields.Boolean("Police Academy")
    psc=fields.Boolean("Staff College")
    rab=fields.Boolean("RAB")
    rab=fields.Boolean("RAB")
    missions=fields.One2many("ribbon.medal.mission",'partner_id')
    @api.multi
    @api.onchange('joining',"retired")
    def calculate_service_length(self):
        currentDate=datetime.datetime.now()
        for rec in self:
            if rec.joining:
                if rec.retired:
                    curYear=rec.retired.year
                    curMonth=rec.retired.month
                    curDay=rec.retired.day
                else:
                    curYear = currentDate.year
                    curMonth = currentDate.month
                    curDay = currentDate.day

                lyear=rec.joining.year
                lmonth=rec.joining.month
                lday=rec.joining.day
                lday=curDay-lday
                lmonth=curMonth-lmonth
                lyear=curYear-lyear
                length_string=""
                if lday<0:
                    lday=lday+30
                    lmonth=lmonth-1
                if lmonth<0:
                    lmonth=lmonth+12
                    lyear=lyear-1
                if lyear>0:
                    length_string=length_string+ str(lyear) +" Year "
                if lmonth>0:
                    length_string=length_string+ str(lmonth) + " Month "
                if lday>0:
                    length_string=length_string+ str(lday) + " Day "
                rec.service_length=length_string
                rec.service_year=lyear
                rec.service_month=lmonth
                rec.service_day=lday

# class RibonMedalPersonalAcquisition(models.Model)
#     _name="ribbon.medal.personal.acquisition"
#     _description = "Personal acquisition for a force member"
#     force_member=fields.Many2one("res.partner","Name")
#     acquired_ribbons=fields.Many2many('ribbon_acquired',)
class RibbonMedalPersonalAward(models.Model):
    _name="ribbon.medal.personal.award"
    _description="list of Personal Award"
    ribbon_holder_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.medal.regulation")
    extension = fields.Many2one("ribbon.medal.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalMission(models.Model):
    _name="ribbon.medal.personal.mission"
    _description="list of Personal Mission"
    ribbon_holder_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.medal.regulation")
    extension = fields.Many2one("ribbon.medal.extension")
    serial = fields.Integer("serial")