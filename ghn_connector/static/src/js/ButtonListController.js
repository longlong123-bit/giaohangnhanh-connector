/** @odoo-module **/

import { useService } from '@web/core/utils/hooks';
import { ListController } from "@web/views/list/list_controller";

export class ButtonListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.rpc = useService("rpc");
    }
    async onClickSyncProvince() {
        const action = await this.orm.call('ghn.province', 'sync_provinces');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
    async onClickSyncDistrict() {
        const action = await this.orm.call('ghn.district', 'sync_districts');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})},
        });
    }
    async onClickSyncWard() {
        const action = await this.orm.call('ghn.ward', 'sync_wards');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
    async onClickSyncService() {
        const action = await this.orm.call('ghn.service', 'sync_service');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
    async onClickSyncStore() {
        const action = await this.orm.call('ghn.store', 'sync_stores');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
    async onClickCreateStore() {
        const action = await this.orm.call('create.store.wizard', 'create_store');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
    async onClickSyncPostOffices() {
        const action = await this.orm.call('ghn.post.office', 'sync_offices');
        this.actionService.doAction(action, {
            onClose: () => {
                this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload'})
            },
        });
    }
}