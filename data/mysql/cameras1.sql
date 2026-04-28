-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Apr 28, 2026 at 08:46 AM
-- Server version: 8.0.45
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cameras1`
--

-- --------------------------------------------------------

--
-- Table structure for table `cache`
--

CREATE TABLE `cache` (
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expiration` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cache`
--

INSERT INTO `cache` (`key`, `value`, `expiration`) VALUES
('laravel-cache-camera_auth_1', 'a:2:{s:8:\"username\";s:7:\"CR-N100\";s:8:\"password\";s:14:\"CR-N100CR-N100\";}', 1768913619),
('laravel-cache-camera_auth_30', 'a:2:{s:8:\"username\";s:7:\"CR-N100\";s:8:\"password\";s:14:\"CR-N100CR-N100\";}', 1769517355),
('laravel-cache-camera_auth_34', 'a:2:{s:8:\"username\";s:7:\"CR-N100\";s:8:\"password\";s:14:\"CR-N100CR-N100\";}', 1769069070);

-- --------------------------------------------------------

--
-- Table structure for table `cache_locks`
--

CREATE TABLE `cache_locks` (
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expiration` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cameras`
--

CREATE TABLE `cameras` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `resolution` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `rtsp_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `room_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `room_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `image` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cameras`
--

INSERT INTO `cameras` (`id`, `name`, `location`, `ip_address`, `status`, `resolution`, `rtsp_url`, `room_id`, `room_name`, `created_at`, `updated_at`, `image`) VALUES
(1, 'Camera Bãi Xe', 'Bãi đỗ xe ngoài trời', '192.168.1.101', 'active', '', 'rtsp://192.168.64.52:8554/cam2', 'l_room_a', '3年B組', '2025-12-01 01:14:04', '2026-04-22 06:10:03', '/static/uploads/1776838202_644535717_1509970134464086_6911294769202537621_n.jpg'),
(30, 'Camera Văn Phòng', 'Văn phòng làm việc tầng 2', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.64.52:8554/cam2', 'l_room_b', '4年4組', '2025-12-17 00:48:36', '2026-04-22 06:58:33', '/static/uploads/1776841113_architecture-vector-db.png'),
(31, 'Camera Kho Hàng', 'Khu vực kệ hàng trung tâm', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.128.153/rtpstream/config3', 'l_room_c', '2年2組', '2025-12-21 19:57:33', '2026-04-22 06:50:05', '/static/uploads/1776840605_Noel.webp'),
(32, 'camera1_4', 'Camera Giám Sát Bãi Xe', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.128.153/rtpstream/config1', 'l_room_d', '3年3組', '2025-12-23 21:16:17', '2026-04-22 07:04:17', '/static/uploads/1776841135_Noel.webp'),
(34, 'camera2', 'Camera Giám Sát Bãi Xe', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.128.54/rtpstream/config1', 'l_room2a', 'room2a', '2026-01-06 18:03:43', '2026-04-22 06:48:37', '/static/uploads/1776840517_ChatGPT_Image_Apr_13_2026_08_55_28_AM.png'),
(35, 'WansviewQ5', 'Camera Giám Sát Bãi Xe', '192.168.64.22', 'active', '1920x1080', 'rtsp://user:1234567890@192.168.129.51:554/live/ch0', 'l_room3', 'room3', '2026-01-12 20:28:08', '2026-04-22 06:48:23', '/static/uploads/1776840503_052095c1-2617-40f4-b54c-735206271318.jpg'),
(36, 'camera1_5', 'Camera Giám Sát Bãi Xe', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.128.153/rtpstream/config1', 'l_room1_5', 'l_room1_5', '2026-01-13 01:32:53', '2026-04-22 06:44:05', '/static/uploads/1776840245_choose-your-side-aeterna-noctis-players-upvote-for-the-king-v0-uhw61rvvwvja1.jpg'),
(37, 'Bạn có thể vào lại', 'Bạn có thể vào lại', '192.168.64.22', 'active', '1920x1080', 'rtsp://192.168.64.52:8554/cam2', 'l_room_6', 'l_room_6', '2026-03-12 20:25:37', '2026-04-22 06:11:47', '/static/uploads/1776838307_644535717_1509970134464086_6911294769202537621_n.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `connection` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `exception` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `queue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `attempts` tinyint UNSIGNED NOT NULL,
  `reserved_at` int UNSIGNED DEFAULT NULL,
  `available_at` int UNSIGNED NOT NULL,
  `created_at` int UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `job_batches`
--

CREATE TABLE `job_batches` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_jobs` int NOT NULL,
  `pending_jobs` int NOT NULL,
  `failed_jobs` int NOT NULL,
  `failed_job_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `options` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `cancelled_at` int DEFAULT NULL,
  `created_at` int NOT NULL,
  `finished_at` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int UNSIGNED NOT NULL,
  `migration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '0001_01_01_000000_create_users_table', 1),
(2, '0001_01_01_000001_create_cache_table', 1),
(3, '0001_01_01_000002_create_jobs_table', 1),
(6, '2025_12_01_065401_create_cameras_table', 2),
(7, '2025_12_18_060257_create_room_status_table', 3),
(8, '2025_12_29_015949_add_is_admin_recording_to_cameras_table', 4),
(9, '2025_12_29_020016_add_is_teacher_recording_to_room_status_table', 4),
(10, '2026_01_16_082600_remove_is_recording_from_room_status_table', 5),
(11, '2026_01_16_091330_remove_is_recording_from_cameras_table', 5);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `room_status`
--

CREATE TABLE `room_status` (
  `id` bigint UNSIGNED NOT NULL,
  `camera_id` bigint UNSIGNED NOT NULL,
  `is_streaming` tinyint UNSIGNED NOT NULL DEFAULT '0' COMMENT '配信状態フラグ',
  `streaming_layout` tinyint UNSIGNED NOT NULL DEFAULT '0' COMMENT '配信レイアウト種別',
  `video_source` tinyint UNSIGNED NOT NULL DEFAULT '0' COMMENT '現在使用中の映像ソース',
  `video_source_right` tinyint UNSIGNED NOT NULL DEFAULT '0' COMMENT '現在使用中の映像ソース',
  `audio_mixer` json DEFAULT NULL COMMENT 'オーディオミキサー設定（JSON形式）',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `room_status`
--

INSERT INTO `room_status` (`id`, `camera_id`, `is_streaming`, `streaming_layout`, `video_source`, `video_source_right`, `audio_mixer`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 2, 3, 2, '{\"mic\": true, \"ipcam\": false, \"system\": true}', '2025-12-18 01:21:14', '2026-03-19 08:27:27'),
(2, 30, 0, 2, 3, 1, '{\"mic\": false, \"ipcam\": false, \"system\": false}', '2025-12-18 20:37:46', '2026-03-16 17:51:00'),
(3, 31, 0, 1, 2, 1, '{\"mic\": false, \"ipcam\": false, \"system\": false}', '2025-12-23 01:48:57', '2026-01-15 23:19:52'),
(5, 34, 0, 1, 1, 1, '{\"mic\": true, \"ipcam\": true, \"system\": false}', '2026-01-06 18:08:13', '2026-01-21 19:13:02'),
(6, 32, 1, 2, 1, 2, '{\"mic\": false, \"ipcam\": false, \"system\": false}', '2026-01-06 19:44:57', '2026-03-12 19:57:12'),
(7, 35, 1, 2, 3, 2, '{\"mic\": true, \"ipcam\": false, \"system\": true}', '2026-01-12 20:47:22', '2026-03-10 23:13:56'),
(8, 36, 0, 2, 3, 2, '{\"mic\": true, \"ipcam\": false, \"system\": false}', '2026-01-13 01:33:27', '2026-03-27 07:34:44'),
(9, 37, 1, 2, 2, 1, '{\"mic\": false, \"ipcam\": false, \"system\": false}', '2026-03-12 22:45:55', '2026-03-27 08:56:28');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `payload` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_activity` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `user_id`, `ip_address`, `user_agent`, `payload`, `last_activity`) VALUES
('8MKa9ELgilLXFhL3TaKiby1GTwp7441avGBXzaFF', NULL, '192.168.64.52', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiSFhXemVEdGxuNkVkaUhRbnhkY1czUEV4RzdJWGd1U3VpQ0hUb3NlcCI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwODAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1765524122),
('bPKgjVlOT0HDxOJOOf6oSL2WAxGxKLX9kMvuttsW', NULL, '192.168.64.27', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiRnVDQ213dFQwTXZlRDAwbjFhU3FZVnFhUjNpTnh6U2ljc3lQd0NNUiI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjI3OjgwMDAiO3M6NToicm91dGUiO3M6Mjc6ImdlbmVyYXRlZDo6UXgzbnZmekpwaGZoaWxkNiI7fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1773802121),
('DO755gNq71ZWkkKRJ4vAHFIEZRKBM0ARlDh5CZ0e', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiemRJUVZTS1VNNTJzZ2x2T3NMY3JVYmpoUVFOQVFIUEtyUjNnRzFYaSI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjE6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMCI7czo1OiJyb3V0ZSI7Tjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319fQ==', 1764575531),
('IuJrMhYAWEHBpEFnHBDfIg3wa2u0Rzi7aZIIZpfA', NULL, '192.168.64.52', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiRVdnOVhxVmJVU0ZBS1RnUG1uek9RVmRuQngwSFhMOTVJT3Q5NDE4YyI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwMDAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1764809192),
('Jdi6hoSacnsvfEPX92xxV9o7JE84RRqxsVvFNzQm', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiVnVKdTBIeUxLSlF4TlZDejllV1MzZzROTEJzSDFTa0tLbUNjNkhuViI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjE6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMCI7czo1OiJyb3V0ZSI7Tjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319fQ==', 1764724147),
('jFtIMeSQm4eQoYYi9aDicl14SNV6UDGeX0qIN6XB', NULL, '192.168.64.52', 'PostmanRuntime/7.49.1', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiWXUwdkpZVW1MYVhuRVJIbDBoelVUZ2M5WU1INExlcnI5N3VJd3dLUSI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwMDAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1764809392),
('JOsKCD5207ghroTe1Wqzfun9qAYO2KTfmsd9qrI4', NULL, '192.168.64.52', 'PostmanRuntime/7.49.1', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoicDNaaVRYVjRUSksyeXIwanIyTW1wNWpHVUJCMzN3aFZseHVURURHNyI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwMDAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1764752193),
('kRCnMTqWxREZ7U8zhiyjpnG0jTAzwp4JF2KrByLq', NULL, '192.168.64.52', 'PostmanRuntime/7.49.1', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiOUtCTnBPRVlwNk9ZaHltaVFKVUpveTNEYVNUc05HdW5nR01nVmJBNiI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwMDAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1764658452),
('lhaaEXV9x2KjyDL91IoEJ3nJdACe89K4A2l51xyv', NULL, '192.168.64.24', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoib29VWGhuUWJZVmJkdjhjcmZvcjE5WDJRV1hrcHQ2VjhSRjdSVTdyeSI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwODAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1773017909),
('oIcoKWTLsUyyhXcb5gaa9D6KzxawF1XNEtUXz5Xy', NULL, '192.168.64.52', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiWFNMd1gzZlB3R05GdHFmUXZwRU1CdE5SN0lwaWk5SlZlajhYUkJuQSI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjU6Imh0dHA6Ly8xOTIuMTY4LjY0LjUyOjgwODAiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1766115083),
('qxahTaosmlTeO3NH1Q9j5IjhnSY23vtuIXvAXHnx', NULL, '127.0.0.1', 'PostmanRuntime/7.49.1', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoicnlUcFl3cmpJT1pCZXozUkZidDBicGR2bzZRNG9oTDZNNUlDSHlvUSI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjE6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMCI7czo1OiJyb3V0ZSI7Tjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319fQ==', 1764576118),
('vNsIpsvIhpJINL2hKuwmyUu1nuuYRxAqxEFMlaH5', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoic0huQmNVek9LMG9rRFR5dDV2SVhsbDNTSVZLOG1VYTh5SkhBN2dEMCI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MjE6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMCI7czo1OiJyb3V0ZSI7Tjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319fQ==', 1764636896);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cameras`
--
ALTER TABLE `cameras`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `job_batches`
--
ALTER TABLE `job_batches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `room_status`
--
ALTER TABLE `room_status`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_status_camera_id_foreign` (`camera_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cameras`
--
ALTER TABLE `cameras`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `room_status`
--
ALTER TABLE `room_status`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `room_status`
--
ALTER TABLE `room_status`
  ADD CONSTRAINT `room_status_camera_id_foreign` FOREIGN KEY (`camera_id`) REFERENCES `cameras` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
