export type Message = {
    id: string;
    created_at: string;
    message: string;
    type: 'user'|'bot'
}