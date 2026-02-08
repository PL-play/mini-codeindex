package com.example;

/**
 * 通知服务类
 * 处理各种通知发送
 */
public class NotificationService {

    public void sendEmail(String to, String subject, String message) {
        // 发送邮件逻辑
        System.out.println("Sending email to: " + to + " with subject: " + subject);
    }

    public void sendSMS(String phoneNumber, String message) {
        // 发送短信逻辑
        System.out.println("Sending SMS to: " + phoneNumber + " with message: " + message);
    }

    public void sendPushNotification(String deviceId, String message) {
        // 发送推送通知逻辑
        System.out.println("Sending push notification to: " + deviceId + " with message: " + message);
    }
}