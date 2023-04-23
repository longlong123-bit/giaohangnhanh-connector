odoo.define('giaohangnhanh_connector.handle_button_ghn', function (require) {
    "use strict";
    var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons.on('click', '.o_ghn_button_sync_province', this._onClickSyncProvinceGHN.bind(this));
                this.$buttons.on('click', '.o_ghn_button_sync_district', this._onClickSyncDistrict.bind(this));
                this.$buttons.on('click', '.o_ghn_button_sync_ward', this._onClickSyncWard.bind(this));
                this.$buttons.on('click', '.o_ghn_button_sync_office', this._onClickSyncOffice.bind(this));
                this.$buttons.on('click', '.o_ghn_button_sync_service', this._onClickSyncService.bind(this));
                this.$buttons.on('click', '.o_ghn_button_sync_store', this._onClickSyncStore.bind(this));
            }
        },
        _onClickSyncProvinceGHN: function (e) {
            var self = this;
            console.log(e)
            return this._rpc({
                model: 'giaohangnhanh.province',
                method: 'sync_provinces'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        },
        _onClickSyncDistrict: function (e) {
            var self = this;
            return this._rpc({
                model: 'giaohangnhanh.district',
                method: 'sync_districts'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        },
        _onClickSyncWard: function (e) {
            var self = this;
            return this._rpc({
                model: 'giaohangnhanh.ward',
                method: 'sync_wards'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        },
        _onClickSyncService: function (e) {
            var self = this;
            return this._rpc({
                model: 'giaohangnhanh.service',
                method: 'sync_services'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        },
        _onClickSyncOffice: function (e) {
            var self = this;
            return this._rpc({
                model: 'giaohangnhanh.office',
                method: 'sync_offices'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        },
        _onClickSyncStore: function (e) {
            var self = this;
            return this._rpc({
                model: 'giaohangnhanh.store',
                method: 'sync_stores'
            }).then(function(result) {
                self.do_action(result);
            }).then(function(result) {
                self.do_action({
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                });
            });
        }
    });
});
