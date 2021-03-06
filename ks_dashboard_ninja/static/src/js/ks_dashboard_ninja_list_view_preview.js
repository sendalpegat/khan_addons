eagle.define('ks_dashboard_ninja_list.ks_dashboard_ninja_list_view_preview', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');

    var QWeb = core.qweb;
    var field_utils = require('web.field_utils');

    var KsListViewPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.state = {};
        },

        _render: function () {
            this.$el.empty()
            var rec = this.recordData;
            if (rec.ks_dashboard_item_type === 'ks_list_view') {
                if(rec.ks_list_view_type=="ungrouped"){
                    if (rec.ks_list_view_fields.count !== 0) {
                        this.ksRenderListView();
                    } else {
                        this.$el.append($('<div>').text("Select Fields to show in list view."));

                    }
                }else if(rec.ks_list_view_type=="grouped"){
                    if (rec.ks_list_view_group_fields.count !== 0 && rec.ks_chart_relation_groupby ) {
                        if(rec.ks_chart_groupby_type ==='relational_type' || rec.ks_chart_groupby_type ==='selection'  || rec.ks_chart_groupby_type ==='date_type' && rec.ks_chart_date_groupby){
                            this.ksRenderListView();
                        }else{
                            this.$el.append($('<div>').text("Select Group by Date to show list data."));
                        }

                    } else {
                        this.$el.append($('<div>').text("Select Fields and Group By to show in list view."));

                    }
                }

            }
        },

        ksRenderListView: function () {
            var field = this.recordData;
            var ks_list_view_name;
            var list_view_data = JSON.parse(field.ks_list_view_data);
            if (field.name) ks_list_view_name = field.name;
            else if (field.ks_model_name) ks_list_view_name = field.ks_model_id.data.display_name;
            else ks_list_view_name = "Name";
            if( field.ks_list_view_type === "ungrouped" && list_view_data){
                var index_data = list_view_data.date_index;
                for (var i = 0; i < index_data.length; i++){
                    for (var j = 0; j < list_view_data.data_rows.length; j++){
                        var index = index_data[i]
                        var date = list_view_data.data_rows[j]["data"][index]
                        list_view_data.data_rows[j]["data"][index] = field_utils.format.datetime(moment(new Date(date+" UTC")), {}, {timezone: false});
                    }
                }
            }

            if (field.ks_list_view_data){
                var data_rows = list_view_data.data_rows;
                for (var i = 0; i < list_view_data.data_rows.length; i++){
                    for (var j = 0; j < list_view_data.data_rows[0]["data"].length; j++){
                        if(typeof(data_rows[i].data[j]) === "number"){
                            list_view_data.data_rows[i].data[j]  = field_utils.format.float(data_rows[i].data[j], Float64Array)
                        }
                    }
                }
            }
            else list_view_data = false;

            var $listViewContainer = $(QWeb.render('ks_list_view_container', {
                ks_list_view_name: ks_list_view_name,
                list_view_data: list_view_data
            }));
            this.$el.append($listViewContainer);

        },

    });
    registry.add('ks_dashboard_list_view_preview', KsListViewPreview);

    return {
        KsListViewPreview: KsListViewPreview,
    };

});