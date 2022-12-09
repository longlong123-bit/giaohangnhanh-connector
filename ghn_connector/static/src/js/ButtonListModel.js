/** @odoo-module */

import { RelationalModel, DynamicRecordList } from "@web/views/relational_model";

export class ButtonListModel extends RelationalModel {

    /**
     * Override
     */
    setup(params, { action, dialog, notification, rpc, user, view, company }) {
        // model has not created any record yet
        this.lastCreatedRecordId = "";
        return super.setup(...arguments);
    }
}

export class ButtonListDynamicRecordList extends DynamicRecordList {

    /**
     * Override
     */
    async createRecord(params = {}, atFirstPosition = false) {
        const record = await super.createRecord(...arguments);
        // keep created record id on model
        record.model.lastCreatedRecordId = record.id;
        return record;
    }
}

ButtonListModel.DynamicRecordList = ButtonListDynamicRecordList;