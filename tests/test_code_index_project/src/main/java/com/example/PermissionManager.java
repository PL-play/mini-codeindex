package com.example;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * 权限管理器
 * 负责用户权限的分配、检查和撤销
 */
public class PermissionManager {
    private final Map<String, Set<String>> userPermissions;
    private final Map<String, Set<String>> rolePermissions;
    private final Map<String, Set<String>> userRoles;
    private final Map<String, PermissionRule> permissionRules;

    // 权限常量
    public static final String READ_USER = "user:read";
    public static final String WRITE_USER = "user:write";
    public static final String DELETE_USER = "user:delete";
    public static final String ADMIN_USER = "user:admin";

    public static final String READ_DEPARTMENT = "department:read";
    public static final String WRITE_DEPARTMENT = "department:write";

    public static final String READ_REPORT = "report:read";
    public static final String WRITE_REPORT = "report:write";

    public static final String SYSTEM_ADMIN = "system:admin";

    // 角色常量
    public static final String ROLE_USER = "USER";
    public static final String ROLE_MANAGER = "MANAGER";
    public static final String ROLE_ADMIN = "ADMIN";
    public static final String ROLE_SUPER_ADMIN = "SUPER_ADMIN";

    public PermissionManager() {
        this.userPermissions = new ConcurrentHashMap<>();
        this.rolePermissions = new ConcurrentHashMap<>();
        this.userRoles = new ConcurrentHashMap<>();
        this.permissionRules = new ConcurrentHashMap<>();

        initializeDefaultRoles();
        initializeDefaultRules();
    }

    /**
     * 初始化默认角色
     */
    private void initializeDefaultRoles() {
        // USER 角色
        Set<String> userPerms = new HashSet<>(Arrays.asList(
            READ_USER, READ_DEPARTMENT, READ_REPORT
        ));
        rolePermissions.put(ROLE_USER, userPerms);

        // MANAGER 角色
        Set<String> managerPerms = new HashSet<>(Arrays.asList(
            READ_USER, WRITE_USER, READ_DEPARTMENT, WRITE_DEPARTMENT, READ_REPORT, WRITE_REPORT
        ));
        rolePermissions.put(ROLE_MANAGER, managerPerms);

        // ADMIN 角色
        Set<String> adminPerms = new HashSet<>(Arrays.asList(
            READ_USER, WRITE_USER, DELETE_USER, ADMIN_USER,
            READ_DEPARTMENT, WRITE_DEPARTMENT,
            READ_REPORT, WRITE_REPORT
        ));
        rolePermissions.put(ROLE_ADMIN, adminPerms);

        // SUPER_ADMIN 角色
        Set<String> superAdminPerms = new HashSet<>(Arrays.asList(
            SYSTEM_ADMIN
        ));
        superAdminPerms.addAll(adminPerms);
        rolePermissions.put(ROLE_SUPER_ADMIN, superAdminPerms);
    }

    /**
     * 初始化默认规则
     */
    private void initializeDefaultRules() {
        // 规则示例：管理员可以管理所有用户
        permissionRules.put("admin_manage_all", new PermissionRule(
            Arrays.asList(ADMIN_USER),
            "user_id != principal_id",
            PermissionEffect.ALLOW
        ));

        // 规则：用户只能修改自己的信息
        permissionRules.put("user_self_modify", new PermissionRule(
            Arrays.asList(WRITE_USER),
            "user_id == principal_id",
            PermissionEffect.ALLOW
        ));

        // 规则：经理可以管理本部门用户
        permissionRules.put("manager_department_users", new PermissionRule(
            Arrays.asList(WRITE_USER),
            "user_department == principal_department",
            PermissionEffect.ALLOW
        ));
    }

    /**
     * 分配角色给用户
     */
    public void assignRole(String userId, String role) {
        userRoles.computeIfAbsent(userId, k -> new HashSet<>()).add(role);
        updateUserPermissions(userId);
    }

    /**
     * 撤销用户角色
     */
    public void revokeRole(String userId, String role) {
        Set<String> roles = userRoles.get(userId);
        if (roles != null) {
            roles.remove(role);
            updateUserPermissions(userId);
        }
    }

    /**
     * 直接分配权限给用户
     */
    public void grantPermission(String userId, String permission) {
        userPermissions.computeIfAbsent(userId, k -> new HashSet<>()).add(permission);
    }

    /**
     * 撤销用户权限
     */
    public void revokePermission(String userId, String permission) {
        Set<String> permissions = userPermissions.get(userId);
        if (permissions != null) {
            permissions.remove(permission);
        }
    }

    /**
     * 检查用户是否有权限
     */
    public boolean hasPermission(String userId, String permission) {
        // 检查直接权限
        Set<String> directPerms = userPermissions.get(userId);
        if (directPerms != null && directPerms.contains(permission)) {
            return true;
        }

        // 检查角色权限
        Set<String> userRoleSet = userRoles.get(userId);
        if (userRoleSet != null) {
            for (String role : userRoleSet) {
                Set<String> rolePerms = rolePermissions.get(role);
                if (rolePerms != null && rolePerms.contains(permission)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * 检查用户是否有任何权限
     */
    public boolean hasAnyPermission(String userId, Collection<String> permissions) {
        return permissions.stream().anyMatch(perm -> hasPermission(userId, perm));
    }

    /**
     * 检查用户是否有所有权限
     */
    public boolean hasAllPermissions(String userId, Collection<String> permissions) {
        return permissions.stream().allMatch(perm -> hasPermission(userId, perm));
    }

    /**
     * 获取用户的所有权限
     */
    public Set<String> getUserPermissions(String userId) {
        Set<String> allPermissions = new HashSet<>();

        // 直接权限
        Set<String> directPerms = userPermissions.get(userId);
        if (directPerms != null) {
            allPermissions.addAll(directPerms);
        }

        // 角色权限
        Set<String> userRoleSet = userRoles.get(userId);
        if (userRoleSet != null) {
            for (String role : userRoleSet) {
                Set<String> rolePerms = rolePermissions.get(role);
                if (rolePerms != null) {
                    allPermissions.addAll(rolePerms);
                }
            }
        }

        return allPermissions;
    }

    /**
     * 获取用户的角色
     */
    public Set<String> getUserRoles(String userId) {
        return new HashSet<>(userRoles.getOrDefault(userId, Collections.emptySet()));
    }

    /**
     * 创建自定义角色
     */
    public void createRole(String roleName, Set<String> permissions) {
        rolePermissions.put(roleName, new HashSet<>(permissions));
    }

    /**
     * 删除角色
     */
    public void deleteRole(String roleName) {
        rolePermissions.remove(roleName);
        // 从所有用户中移除该角色
        userRoles.values().forEach(roles -> roles.remove(roleName));
    }

    /**
     * 更新角色权限
     */
    public void updateRolePermissions(String roleName, Set<String> permissions) {
        rolePermissions.put(roleName, new HashSet<>(permissions));
        // 更新所有拥有该角色的用户的权限
        userRoles.entrySet().stream()
            .filter(entry -> entry.getValue().contains(roleName))
            .forEach(entry -> updateUserPermissions(entry.getKey()));
    }

    /**
     * 添加权限规则
     */
    public void addPermissionRule(String ruleId, PermissionRule rule) {
        permissionRules.put(ruleId, rule);
    }

    /**
     * 删除权限规则
     */
    public void removePermissionRule(String ruleId) {
        permissionRules.remove(ruleId);
    }

    /**
     * 高级权限检查（考虑规则）
     */
    public boolean checkPermissionWithRules(String userId, String permission,
                                          Map<String, Object> context) {
        // 首先检查基本权限
        if (!hasPermission(userId, permission)) {
            return false;
        }

        // 应用规则
        for (PermissionRule rule : permissionRules.values()) {
            if (rule.permissions.contains(permission)) {
                PermissionEffect effect = evaluateRule(rule, userId, context);
                if (effect == PermissionEffect.DENY) {
                    return false;
                } else if (effect == PermissionEffect.ALLOW) {
                    return true;
                }
            }
        }

        return true;
    }

    /**
     * 评估权限规则
     */
    private PermissionEffect evaluateRule(PermissionRule rule, String userId,
                                        Map<String, Object> context) {
        // 简化实现：这里应该有完整的表达式评估器
        // 实际实现需要解析 rule.condition 并根据 context 评估

        // 示例：如果条件是 "user_id == principal_id"
        if ("user_id == principal_id".equals(rule.condition)) {
            String targetUserId = (String) context.get("user_id");
            return targetUserId != null && targetUserId.equals(userId) ?
                   rule.effect : PermissionEffect.NEUTRAL;
        }

        return PermissionEffect.NEUTRAL;
    }

    /**
     * 获取所有角色
     */
    public Set<String> getAllRoles() {
        return new HashSet<>(rolePermissions.keySet());
    }

    /**
     * 获取角色的权限
     */
    public Set<String> getRolePermissions(String role) {
        return new HashSet<>(rolePermissions.getOrDefault(role, Collections.emptySet()));
    }

    /**
     * 获取有特定权限的所有用户
     */
    public Set<String> getUsersWithPermission(String permission) {
        return userPermissions.entrySet().stream()
            .filter(entry -> entry.getValue().contains(permission))
            .map(Map.Entry::getKey)
            .collect(Collectors.toSet());
    }

    /**
     * 获取有特定角色的所有用户
     */
    public Set<String> getUsersWithRole(String role) {
        return userRoles.entrySet().stream()
            .filter(entry -> entry.getValue().contains(role))
            .map(Map.Entry::getKey)
            .collect(Collectors.toSet());
    }

    /**
     * 批量分配角色
     */
    public void bulkAssignRole(Collection<String> userIds, String role) {
        for (String userId : userIds) {
            assignRole(userId, role);
        }
    }

    /**
     * 批量撤销角色
     */
    public void bulkRevokeRole(Collection<String> userIds, String role) {
        for (String userId : userIds) {
            revokeRole(userId, role);
        }
    }

    /**
     * 更新用户权限缓存
     */
    private void updateUserPermissions(String userId) {
        // 这里可以实现权限缓存更新逻辑
        // 简化实现
    }

    /**
     * 权限规则类
     */
    public static class PermissionRule {
        public final List<String> permissions;
        public final String condition;
        public final PermissionEffect effect;

        public PermissionRule(List<String> permissions, String condition, PermissionEffect effect) {
            this.permissions = new ArrayList<>(permissions);
            this.condition = condition;
            this.effect = effect;
        }
    }

    /**
     * 权限效果枚举
     */
    public enum PermissionEffect {
        ALLOW, DENY, NEUTRAL
    }

    /**
     * 权限检查结果
     */
    public static class PermissionCheckResult {
        public final boolean granted;
        public final String reason;
        public final List<String> appliedRules;

        public PermissionCheckResult(boolean granted, String reason, List<String> appliedRules) {
            this.granted = granted;
            this.reason = reason;
            this.appliedRules = new ArrayList<>(appliedRules);
        }
    }
}