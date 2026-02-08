package com.example;

/**
 * 数据处理器类
 * 处理各种数据操作
 */
public class DataProcessor {

    public void processData(String data) {
        // 数据处理逻辑
        System.out.println("Processing data: " + data);
    }

    public String transformData(String input) {
        // 数据转换逻辑
        return input.toUpperCase();
    }

    public boolean validateData(String data) {
        // 数据验证逻辑
        return data != null && !data.trim().isEmpty();
    }
}