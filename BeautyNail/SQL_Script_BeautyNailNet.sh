# ********************************
# Project Phase II
# Team 7 Bao Thinh Diep - Linda Miao
# This script combine bash script with sql script
# because our should run the python manage.py migrate first
# to create django tables and then link the customer table
# with auth_user table of django for login feature.
# ********************************

#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
DB_NAME="beautynailnet"
DB_USER="root"
DB_PASS="root"
DB_HOST="127.0.0.1"
DB_PORT="3306"

# 1) Ensure DB exists (Django cannot do this part)
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" \
  -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# 2) Run Django migrations (creates auth_user and the other Django tables)
python manage.py migrate

# 3) Load your whole app schema + data in one go
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<'SQL'

--
-- Database: `beautynailnet`
--

CREATE DATABASE beautynailnet;
USE beautynailnet;


-- ************************************ --
--               Part A                 --
-- There are 9 tables for our database --
-- ************************************ --

-- table customer: store data about the customers of the nail spa
CREATE TABLE IF NOT EXISTS `CUSTOMER` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `allergies` text,
  `preferred_color` varchar(50) DEFAULT NULL,
  `loyalty_points` int DEFAULT '0',
  `registration_date` date DEFAULT (curdate()),
  `is_active` tinyint(1) DEFAULT '1',
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_customer_user_id` (`user_id`),
  CONSTRAINT `fk_customer_user`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  AUTO_INCREMENT = 21;


-- table staff: store data about all staff in the nail spa
CREATE TABLE IF NOT EXISTS `STAFF` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hire_date` date NOT NULL,
  `position` varchar(50) NOT NULL,
  `commission_rate` decimal(5,2) DEFAULT '0.15',
  `specialty` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  AUTO_INCREMENT = 12;


-- table service: store data about all the services provided by the nail spa
CREATE TABLE IF NOT EXISTS `SERVICE` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `description` text,
  `base_price` decimal(8,2) NOT NULL,
  `duration_minutes` int NOT NULL,
  `category` varchar(50) NOT NULL,
  `requies_appointment` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- table inventory: store data about products available in the nail spa
CREATE TABLE IF NOT EXISTS `INVENTORY` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `category` varchar(50) NOT NULL,
  `color_name` varchar(50) DEFAULT NULL,
  `quantity_in_stock` int DEFAULT '0',
  `unit_cost` decimal(6,2) NOT NULL,
  `retail_price` decimal(6,2) DEFAULT NULL,
  `reorder_level` int DEFAULT '5',
  `supplier_name` varchar(100) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- table events: store the data about events provided by the nail spa
CREATE TABLE IF NOT EXISTS `EVENTS` (
  `events_id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(100) NOT NULL,
  `description` text,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`events_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- table appointment: store data of all appointments with customers
CREATE TABLE IF NOT EXISTS `APPOINTMENT` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time DEFAULT NULL,
  `status` varchar(20) DEFAULT 'scheduled',
  `total_amount` decimal(8,2) DEFAULT NULL,
  `notes` text,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointment_id`),
  FOREIGN KEY (`customer_id`) REFERENCES `CUSTOMER` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`staff_id`) REFERENCES `STAFF` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  AUTO_INCREMENT = 21;

-- table appointment_service: store data about the detailed services related to the appointment
CREATE TABLE IF NOT EXISTS `APPOINTMENT_SERVICE` (
  `appointment_service_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `service_id` int NOT NULL,
  `service_price` decimal(8,2) NOT NULL,
  `polish_color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`appointment_service_id`),
  FOREIGN KEY (`appointment_id`) REFERENCES `APPOINTMENT` (`appointment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`service_id`) REFERENCES `SERVICE` (`service_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  AUTO_INCREMENT = 25;

-- table payment: store data about the payment of each appointment
CREATE TABLE IF NOT EXISTS `PAYMENT` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `tip_amount` decimal(6,2) DEFAULT '0.00',
  `payment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `transaction_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  FOREIGN KEY (`appointment_id`) REFERENCES `APPOINTMENT` (`appointment_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  AUTO_INCREMENT = 11;

-- table review: store data about the reviews by customers 
CREATE TABLE IF NOT EXISTS `REVIEW` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `appointment_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `rating` int NOT NULL,
  `comment` text,
  `review_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- ************************************ --
--               Part B                 --
-- The sample of the data of each table --
-- ************************************ --

--
-- Insert 10 users into auth_user
-- Password hashes generated by Django for 'user1' to 'user10' (password is user1 to user10)
-- 
INSERT INTO `auth_user` (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$1000000$RiWhm3agStyCcbeEGx0h3X$xaDhoqmdHSTO+vCIjUbNLjhIPZaIeKwTu6DI5v/atXA=',NULL, 1, 'admin', 'admin', 'staff', 'admin@gmail.com',1, 1, NOW()),
('pbkdf2_sha256$1000000$Fn0RZNRxwR9BLjcTNEaQqg$vOYXITcbC2NXneAhSk8vXV7F3tQ+SoeJ8w8RkaTyXbQ=', NULL, 0, 'user1',  'Todd',    'Sims',    'todd.sims@email.com',         0, 1, NOW()),
('pbkdf2_sha256$1000000$Vf5uTFBUG9nxzdATuvav0X$wzzEv5e6LswUo7VmNEhnV8rVAju41K5+iDHdVbMqTkw=', NULL, 0, 'user2',  'Robin',   'Harris',  'robin.harris@yahoo.com',      0, 1, NOW()),
('pbkdf2_sha256$1000000$4V1koRe2V5qSyzsU1fbwGb$j3BWDqDbobiWhiEvpX69SzeVRplCeQn2oHaIxZSXGhs=', NULL, 0, 'user3',  'Nancy',   'Deleon',  'nancy.deleon@hotmail.com',    0, 1, NOW()),
('pbkdf2_sha256$1000000$RZhoi9d7lRqMbfkukNWOdc$AVjmRndXuPuVsYw3UteT8l+OZgOnQMngafQVR+JcNrE=', NULL, 0, 'user4',  'Raymond', 'Miller',  'raymond.miller@email.com',    0, 1, NOW()),
('pbkdf2_sha256$1000000$vgpf7yLkYpi43BGGaU4HKU$VxmhyCdN4mm/0DSKUOmO67irkY6lXMx9X8U3LkVSG0M=', NULL, 0, 'user5',  'Alyssa',  'Jackson', 'alyssa.jackson@gmail.com',    0, 1, NOW()),
('pbkdf2_sha256$1000000$tR52LxJ845Py2ZwGDZnqCZ$kzpchf+tULmaUaN8gB5k9qTBa70mecd1BMdYKn5mXrI=', NULL, 0, 'user6',  'Hailey',  'Webb',    'hailey.webb@hotmail.com',     0, 1, NOW()),
('pbkdf2_sha256$1000000$YJmd2XXGv9hQKFvhn6xlBq$oHUkbF54rnv1uSTtvWjhFb68I9kJVAQCsShtp84c2PE=', NULL, 0, 'user7',  'Jessica', 'Irwin',   'jessica.irwin@email.com',     0, 1, NOW()),
('pbkdf2_sha256$1000000$aGRWKyw6JwCHR8wEswoFDh$Tx+Cvuj0XdlI6wUV8qwbEmPPmNEl3RjbY7P9QxcNgaE=', NULL, 0, 'user8',  'Tina',    'Rhodes',  'tina.rhodes@email.com',       0, 1, NOW()),
('pbkdf2_sha256$1000000$HR54YSziabH3tSwIALMsFH$9WaBzwX2pjeov8NgoY/F2aUWMVaKnFdTx6iIsQq2srs=', NULL, 0, 'user9',  'Anne',    'Johnson', 'anne.johnson@hotmail.com',    0, 1, NOW()),
('pbkdf2_sha256$1000000$Vmp6ivWTXOVhaiy6SOnk3q$JaFxHuTe7gRXgtCGRbtpp2Jn6271Lm2Ueqs+ZnvuhWo=', NULL, 0, 'user10', 'Rachel',  'Wheeler', 'rachel.wheeler@email.com',    0, 1, NOW());

--
-- Dumping data for table `CUSTOMER`
--

INSERT INTO `CUSTOMER`
(`customer_id`, `first_name`, `last_name`, `phone`, `email`, `date_of_birth`, `allergies`, `preferred_color`, `loyalty_points`, `registration_date`, `is_active`, `user_id`) VALUES
(11, 'Todd',    'Sims',    '618-845-8073', 'todd.sims@email.com',        '1996-10-11', NULL,        'Purple', 174, '2024-12-31', 1, (SELECT id FROM auth_user WHERE username='user1')),
(12, 'Robin',   'Harris',  '905-579-7081', 'robin.harris@yahoo.com',     '2000-01-19', 'Pollen',    'Red',     86, '2023-01-19', 1, (SELECT id FROM auth_user WHERE username='user2')),
(13, 'Nancy',   'Deleon',  '227-854-9780', 'nancy.deleon@hotmail.com',   '1959-10-27', 'Pollen',    NULL,     289, '2023-11-09', 1, (SELECT id FROM auth_user WHERE username='user3')),
(14, 'Raymond', 'Miller',  '468-626-2871', 'raymond.miller@email.com',   '1960-01-15', 'Fragrance', 'Red',    120, '2023-10-07', 1, (SELECT id FROM auth_user WHERE username='user4')),
(15, 'Alyssa',  'Jackson', '403-441-6240', 'alyssa.jackson@gmail.com',   '1998-10-31', 'Dust',      'Pink',   284, '2025-06-10', 1, (SELECT id FROM auth_user WHERE username='user5')),
(16, 'Hailey',  'Webb',    '906-416-5220', 'hailey.webb@hotmail.com',    '1965-06-06', 'Pollen',    'Red',     10, '2024-01-28', 0, (SELECT id FROM auth_user WHERE username='user6')),
(17, 'Jessica', 'Irwin',   '731-049-6021', 'jessica.irwin@email.com',    '1967-12-17', NULL,        'Red',     16, '2022-09-07', 1, (SELECT id FROM auth_user WHERE username='user7')),
(18, 'Tina',    'Rhodes',  '037-456-5659', 'tina.rhodes@email.com',      '1961-10-10', 'Pollen',    'Green',  144, '2024-01-07', 1, (SELECT id FROM auth_user WHERE username='user8')),
(19, 'Anne',    'Johnson', '866-823-7190', 'anne.johnson@hotmail.com',   '1981-04-27', 'Nail polish remover', 'Pink', 149, '2024-12-09', 1, (SELECT id FROM auth_user WHERE username='user9')),
(20, 'Rachel',  'Wheeler', '407-484-5977', 'rachel.wheeler@email.com',   '1995-03-19', NULL,        'Red',    124, '2023-03-12', 0, (SELECT id FROM auth_user WHERE username='user10'));

--
-- Dumping data for table `STAFF`
--

INSERT INTO `STAFF` (`staff_id`, `first_name`, `last_name`, `phone`, `email`, `hire_date`, `position`, `commission_rate`, `specialty`, `is_active`) VALUES
(1, 'Linda', 'Miao', '206-565-0200', 'linda.miao@beautynailnet.com', '2024-06-13', 'Junior Nail Technician', 0.12, 'Basic Manicures', 1),
(2, 'Emily', 'Rodriguez', '206-555-0201', 'emily.rodriguez@beautynailnet.com', '2023-06-15', 'Senior Nail Technician', 0.20, 'Gel Manicures', 1),
(3, 'Jessica', 'Chen', '206-555-0202', 'jessica.chen@beautynailnet.com', '2023-08-20', 'Nail Technician', 0.15, 'Pedicures', 1),
(4, 'Sophia', 'Kim', '206-555-0203', 'sophia.kim@beautynailnet.com', '2024-01-10', 'Nail Artist', 0.18, 'Nail Art Design', 1),
(5, 'Madison', 'Thompson', '206-555-0204', 'madison.thompson@beautynailnet.com', '2023-09-05', 'Senior Technician', 0.20, 'Acrylic Extensions', 1),
(6, 'Ashley', 'Garcia', '206-555-0205', 'ashley.garcia@beautynailnet.com', '2024-02-01', 'Nail Technician', 0.15, 'Classic Manicures', 1),
(7, 'Taylor', 'White', '206-555-0206', 'taylor.white@beautynailnet.com', '2023-07-12', 'Spa Technician', 0.17, 'Spa Pedicures', 1),
(8, 'Olivia', 'Martinez', '206-555-0207', 'olivia.martinez@beautynailnet.com', '2023-11-20', 'Nail Technician', 0.15, 'French Manicures', 1),
(9, 'Hannah', 'Lee', '206-555-0208', 'hannah.lee@beautynailnet.com', '2024-01-25', 'Junior Technician', 0.12, 'Basic Manicures', 1),
(10, 'Megan', 'Jackson', '206-555-0209', 'megan.jackson@beautynailnet.com', '2023-10-15', 'Manager', 0.25, 'All Services', 1),
(11, 'Rachel', 'Brown', '206-555-0210', 'rachel.brown@beautynailnet.com', '2023-12-01', 'Nail Artist', 0.18, 'Special Occasion Nails', 1);

--
-- Dumping data for table `SERVICE`
--

INSERT INTO `SERVICE` (`service_id`, `service_name`, `description`, `base_price`, `duration_minutes`, `category`, `requies_appointment`) VALUES
(1, 'Polish Change', 'Simple polish removal and new color application', 15.00, 20, 'Basic', 1),
(2, 'Cuticle Treatment', 'Professional cuticle care and conditioning', 20.00, 25, 'Treatment', 1),
(3, 'Paraffin Treatment', 'Moisturizing paraffin wax treatment for hands or feet', 25.00, 30, 'Treatment', 1),
(4, 'Gel Removal', 'Safe removal of existing gel polish', 12.00, 20, 'Removal', 1),
(5, 'Classic Manicure', 'Basic nail shaping, cuticle care, and polish application', 25.00, 45, 'Manicure', 1),
(6, 'Gel Manicure', 'Long-lasting gel polish application with UV curing', 35.00, 60, 'Manicure', 1),
(7, 'French Manicure', 'Classic white tip design with clear or nude base', 30.00, 50, 'Manicure', 1),
(8, 'Acrylic Full Set', 'Complete acrylic nail extension application', 55.00, 90, 'Extensions', 1),
(9, 'Classic Pedicure', 'Foot soak, nail care, and polish with relaxing massage', 40.00, 60, 'Pedicure', 1),
(10, 'Spa Pedicure', 'Deluxe pedicure with exfoliation and extended massage', 60.00, 75, 'Pedicure', 1),
(11, 'Nail Art Design', 'Custom artistic nail designs and decorations', 15.00, 30, 'Art', 1);

--
-- Dumping data for table `INVENTORY`
--

INSERT INTO `INVENTORY` (`inventory_id`, `product_name`, `brand`, `category`, `color_name`, `quantity_in_stock`, `unit_cost`, `retail_price`, `reorder_level`, `supplier_name`, `last_updated`) VALUES
(1, 'OPI Red Polish', 'OPI', 'Polish', 'Big Apple Red', 25, 8.50, 15.00, 5, 'Beauty Supply Co', '2025-07-18 22:09:18'),
(2, 'Essie Pink Polish', 'Essie', 'Polish', 'Ballet Slippers', 20, 7.00, 12.00, 5, 'Nail Distributors', '2025-07-18 22:09:18'),
(3, 'Base Coat', 'CND', 'Treatment', NULL, 15, 6.00, 10.00, 3, 'Professional Nails Inc', '2025-07-18 22:09:18'),
(4, 'Top Coat', 'CND', 'Treatment', NULL, 18, 6.50, 11.00, 3, 'Professional Nails Inc', '2025-07-18 22:09:18'),
(5, 'Nail Files', 'Generic', 'Tools', NULL, 50, 0.75, 2.00, 10, 'Salon Supplies LLC', '2025-07-18 22:09:18'),
(6, 'Cuticle Oil', 'OPI', 'Treatment', NULL, 12, 4.00, 8.00, 3, 'Beauty Supply Co', '2025-07-18 22:09:18'),
(7, 'Cotton Pads', 'Generic', 'Supplies', NULL, 100, 0.25, 1.00, 20, 'General Supply', '2025-07-18 22:09:18'),
(8, 'Acetone', 'Zoya', 'Remover', NULL, 8, 3.00, 6.00, 2, 'Chemical Supply Co', '2025-07-18 22:09:18'),
(9, 'Gel Polish Blue', 'Gelish', 'Gel', 'Ocean Blue', 22, 12.00, 20.00, 5, 'Gel Systems Ltd', '2025-07-18 22:09:18'),
(10, 'Nail Glue', 'Kiss', 'Adhesive', NULL, 30, 1.50, 4.00, 8, 'Nail Repair Co', '2025-07-18 22:09:18');

INSERT INTO `EVENTS` (`events_id`, `event_name`, `description`, `start_date`, `end_date`, `image`) VALUES
(1, 'Spring Blossom Special', 'Celebrate spring with 15% off all floral nail art designs.', '2025-03-20', '2025-04-30', 'images/events/spring_blossom.jpg'),
(2, 'Mother\'s Day Pamper', 'Treat your mom to a deluxe manicure and pedicure combo with a free gift.', '2025-05-01', '2025-05-12', 'images/events/mothers_day.jpg'),
(3, 'Summer Glow Up', 'Discounts on paraffin treatments and gel manicures to prep for summer.', '2025-06-01', '2025-06-30', 'images/events/summer_glow.jpg'),
(4, 'July 4th Nail Fest', 'Red, white, and blue nail art specials for Independence Day!', '2025-07-01', '2025-07-07', 'images/events/july4th.jpg'),
(5, 'Back to School Deals', 'Students get 20% off all basic manicures and pedicures.', '2025-08-15', '2025-09-15', 'images/events/back_to_school.jpg'),
(6, 'Autumn Colors Collection', 'Showcase of seasonal colors and limited edition polishes.', '2025-09-21', '2025-10-31', 'images/events/autumn_colors.jpg'),
(7, 'Halloween Nail Art Contest', 'Win prizes for the spookiest nail designs! Submit photos by Oct 28.', '2025-10-01', '2025-10-31', 'images/events/halloween.jpg'),
(8, 'Thankful Hands', 'Book any treatment in November and get a free cuticle oil sample.', '2025-11-01', '2025-11-30', 'images/events/thanksgiving.jpg'),
(9, 'Holiday Sparkle Week', 'Festive glitter styles and gift card giveaways all December long.', '2025-12-01', '2025-12-24', 'images/events/holiday_sparkle.jpg'),
(10, 'New Year, New Nails', 'Kick off 2026 with 10% off your first appointment of the year.', '2026-01-01', '2026-01-15', 'images/events/new_year.jpg');

--
-- Dumping data for table `APPOINTMENT`
--

INSERT INTO `APPOINTMENT` (`appointment_id`, `customer_id`, `staff_id`, `appointment_date`, `start_time`, `end_time`, `status`, `total_amount`, `notes`, `created_date`) VALUES
(11, 11, 1, '2024-07-22', '09:00:00', '10:00:00', 'scheduled', 45.00, 'First-time client', '2025-07-19 03:52:28'),
(12, 12, 3, '2024-07-22', '10:30:00', '11:30:00', 'completed', 35.00, 'Regular customer', '2025-07-19 03:52:28'),
(13, 13, 2, '2024-07-23', '14:00:00', '15:00:00', 'scheduled', 60.00, 'Spa pedicure', '2025-07-19 03:52:28'),
(14, 14, 1, '2024-07-23', '15:30:00', '16:30:00', 'completed', 25.00, 'Quick polish change', '2025-07-19 03:52:28'),
(15, 15, 4, '2024-07-24', '11:00:00', '12:30:00', 'scheduled', 55.00, 'Acrylic full set', '2025-07-19 03:52:28'),
(16, 16, 2, '2024-07-24', '13:00:00', '14:00:00', 'completed', 30.00, 'French manicure', '2025-07-19 03:52:28'),
(17, 17, 3, '2024-07-25', '09:30:00', '10:30:00', 'scheduled', 40.00, 'Classic pedicure', '2025-07-19 03:52:28'),
(18, 18, 1, '2024-07-25', '14:30:00', '15:30:00', 'completed', 35.00, 'Gel manicure', '2025-07-19 03:52:28'),
(19, 19, 5, '2024-07-26', '10:00:00', '11:00:00', 'scheduled', 25.00, 'Classic manicure', '2025-07-19 03:52:28'),
(20, 20, 2, '2024-07-26', '16:00:00', '17:00:00', 'scheduled', 50.00, 'Nail art design', '2025-07-19 03:52:28');

--
-- Dumping data for table `APPOINTMENT_SERVICE`
--

INSERT INTO `APPOINTMENT_SERVICE` (`appointment_service_id`, `appointment_id`, `service_id`, `service_price`, `polish_color`) VALUES
(13, 11, 1, 25.00, 'Classic Red'),
(14, 11, 7, 20.00, 'Gold accent'),
(15, 12, 2, 35.00, 'Pink Shimmer'),
(16, 13, 6, 60.00, 'French White'),
(17, 14, 9, 15.00, 'Clear'),
(18, 15, 4, 55.00, 'Nude Pink'),
(19, 16, 3, 30.00, 'French White'),
(20, 17, 5, 40.00, 'Ocean Blue'),
(21, 18, 2, 35.00, 'Gel Red'),
(22, 19, 1, 25.00, 'Classic Pink'),
(23, 20, 7, 15.00, 'Silver glitter'),
(24, 20, 1, 25.00, 'Base coat');

--
-- Dumping data for table `PAYMENT`
--

INSERT INTO `PAYMENT` (`payment_id`, `appointment_id`, `payment_method`, `amount`, `tip_amount`, `payment_date`, `transaction_id`) VALUES
(1, 11, 'Credit Card', 45.00, 8.00, '2024-07-22 10:15:00', 'TXN20240722001'),
(2, 12, 'Cash', 35.00, 5.00, '2024-07-22 11:45:00', 'CASH20240722002'),
(3, 13, 'Credit Card', 60.00, 12.00, '2024-07-23 15:15:00', 'TXN20240723003'),
(4, 14, 'Debit Card', 25.00, 3.00, '2024-07-23 16:45:00', 'DBT20240723004'),
(5, 15, 'Credit Card', 55.00, 10.00, '2024-07-24 12:45:00', 'TXN20240724005'),
(6, 16, 'Cash', 30.00, 5.00, '2024-07-24 14:15:00', 'CASH20240724006'),
(7, 17, 'Credit Card', 40.00, 7.00, '2024-07-25 10:45:00', 'TXN20240725007'),
(8, 18, 'Debit Card', 35.00, 6.00, '2024-07-25 15:45:00', 'DBT20240725008'),
(9, 19, 'Cash', 25.00, 4.00, '2024-07-26 11:15:00', 'CASH20240726009'),
(10, 20, 'Credit Card', 40.00, 8.00, '2024-07-26 17:15:00', 'TXN20240726010');

--
-- Dumping data for table `REVIEW`
--

INSERT INTO `REVIEW` (`review_id`, `customer_id`, `appointment_id`, `staff_id`, `rating`, `comment`, `review_date`) VALUES
(1, 11, 11, 1, 5, 'Amazing service! Linda did a fantastic job on my nails. Very professional and friendly.', '2024-07-22 18:30:00'),
(2, 12, 12, 3, 4, 'Good quality work. Jessica was skilled and the salon was clean. Will come back.', '2024-07-22 20:15:00'),
(3, 13, 13, 2, 5, 'Absolutely love my spa pedicure! Emily was so gentle and the massage was relaxing.', '2024-07-23 19:45:00'),
(4, 14, 14, 1, 3, 'Quick service but polish chipped after 2 days. Expected better quality.', '2024-07-24 10:30:00'),
(5, 15, 15, 4, 5, 'Sophia did an incredible job on my acrylic set! Perfect length and shape.', '2024-07-24 20:00:00'),
(6, 16, 16, 2, 4, 'Nice French manicure. Emily was professional and the result looks great.', '2024-07-25 09:15:00'),
(7, 17, 17, 3, 5, 'Best pedicure I have ever had! Jessica was amazing and very thorough.', '2024-07-25 18:30:00'),
(8, 18, 18, 1, 4, 'Good gel manicure. Linda was efficient and the color selection was great.', '2024-07-26 08:45:00'),
(9, 19, 19, 5, 2, 'Service was okay but felt rushed. Manicure was basic, nothing special.', '2024-07-26 15:20:00'),
(10, 20, 20, 2, 5, 'Emily created beautiful nail art! So creative and exactly what I wanted.', '2024-07-27 12:00:00');


-- ************************************ --
--               Part C                 --
--        Designing SQL Queries         --
-- ************************************ --

-- SQL Query 1: Computes a join of at least three tables (must use JOIN ON)
-- Goal: Display customer appointments with assigned staff and service details 
-- Display: Customer names, appointment dates, staff names, and service information

SELECT c.first_name AS customer_first_name,
       c.last_name AS customer_last_name,
       a.appointment_date,
       a.start_time,                    
       s.first_name AS staff_first_name,
       s.last_name AS staff_last_name,
       s.position,
       a.status,
       a.total_amount
FROM CUSTOMER c
JOIN APPOINTMENT a ON c.customer_id = a.customer_id
JOIN STAFF s ON a.staff_id = s.staff_id  
ORDER BY a.appointment_date, a.start_time;


-- SQL Query 2: Uses nested queries with the IN, ANY or ALL operator and uses a GROUP BY clause 
-- Goal: Find customers who have appointments with staff that have commission rates above average 
-- Display: Customer names who worked with high-commission staff members

SELECT c.first_name, c.last_name, COUNT(a.appointment_id) AS appointment_count FROM CUSTOMER c 
JOIN APPOINTMENT a 
ON c.customer_id = a.customer_id 
WHERE a.staff_id IN ( 
SELECT s.staff_id 
FROM STAFF s 
WHERE s.commission_rate > (SELECT AVG(commission_rate) FROM STAFF) 
) 
GROUP BY c.customer_id, c.first_name, c.last_name 
HAVING COUNT(a.appointment_id) >= 1 
ORDER BY appointment_count DESC;


-- SQL Query 3: A correlated nested query with proper aliasing applied alter
-- Goal: Find staff members who have appointments scheduled (correlated with outer query) 
-- Display: Staff names who have at least one appointment.

SELECT s.first_name, s.last_name, s.position, 
                 (SELECT COUNT(*) FROM APPOINTMENT a1
                 WHERE a1.staff_id = s.staff_id) as appointment_count 
FROM STAFF s 
WHERE EXISTS (SELECT 1 
               FROM APPOINTMENT a2 
               WHERE a2.staff_id = s.staff_id) 
ORDER BY appointment_count DESC;

-- SQL Query 4: Uses a FULL OUTER JOIN
-- Goal: Show all customers and all staff, including those without appointments 
-- Display: Complete list showing everyone (customers and staff) regardless of appointment status
SELECT 'Customer' as person_type, c.first_name, c.last_name, a.appointment_date, a.start_time, a.status 
FROM CUSTOMER c 
LEFT JOIN APPOINTMENT a ON c.customer_id = a.customer_id 
-- above is part one shows all customers that include have and have not appointment. (no appointment show customer + NULL)
UNION  -- combine part 1 and part 3
SELECT 'Staff' as person_type, s.first_name, s.last_name, a.appointment_date, a.start_time, a.status 
FROM STAFF s 
LEFT JOIN APPOINTMENT a ON s.staff_id = a.staff_id WHERE s.staff_id 
-- above is part 2 that left join for stadd who do not have any appointment 
NOT IN (SELECT DISTINCT staff_id FROM APPOINTMENT) 
ORDER BY person_type, first_name;

-- SQL Query 5: Uses nested queries with any of the set operations UNION, EXCEPT, or INTERSECT*  
-- Goal: Combine active customers and active staff into one contact list 
-- Display: Complete contact list showing all active people (customers and staff) 

SELECT 'Customer' as contact_type, first_name, last_name, phone, email, 'N/A' as position FROM CUSTOMER WHERE is_active = 1 
UNION 
SELECT 'Staff' as contact_type, first_name, last_name, phone, email, position 
FROM STAFF WHERE is_active = 1 
ORDER BY contact_type, last_name;

-- SQL Query 6: Create your  own non-trivial SQL query (must use at least two tables in FROM clause)  
-- Goal: Show staff members that have the most positive reviews from customers
-- Display: List of staff members that have the most numbers of maximum rating in the review

SELECT staff.staff_id, first_name, last_name, COUNT(*) AS five_star_reviews
FROM review, staff
WHERE rating = 5
AND review.staff_id = staff.staff_id
GROUP BY staff_id
HAVING COUNT(*) = (
  SELECT MAX(staff_review_count) 
  FROM (
    SELECT COUNT(*) AS staff_review_count
    FROM review
    WHERE rating = 5
    GROUP BY staff_id
  ) AS counts
);

-- SQL Query 7: Create your  own non-trivial SQL query (must use at least two tables in FROM clause)  
-- Goal: Show the most favorable staff member of the nail spa
-- Display: List of staff members that have the greatest number of appointments with customers

SELECT staff.staff_id, first_name, last_name, COUNT(*) AS appointments
FROM appointment, staff
WHERE appointment.staff_id = staff.staff_id
GROUP BY staff_id
HAVING COUNT(*) = (
  SELECT MAX(appointment_count) 
  FROM (
    SELECT COUNT(*) AS appointment_count
    FROM appointment
    GROUP BY staff_id
  ) AS counts
);

-- SQL Query 8: Create your  own non-trivial SQL query (must use at least two tables in FROM clause)  
-- Goal: Display customers who gave very negative feedback about the nail salon's service.
-- Display: List of customers who gave a rating below 3 in the reviews and the staff members who associated with those reviews.

SELECT r.appointment_id, r.rating, c.customer_id, c.first_name, c.last_name, s.staff_id, s.first_name, s.last_name
FROM review as r, customer as c, staff as s
WHERE r.customer_id = c.customer_id
AND r.staff_id = s.staff_id
AND rating < 3
ORDER BY rating ASC;

-- SQL Query 9: Create your  own non-trivial SQL query (must use at least three tables in FROM clause)  
-- Goal: Display the customer who brings the highest profit to the nail salon.
-- Display: List of customers who gave the most benefits to the nail salon and the amount of the money they contributed to the business.

SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount + p.tip_amount) AS total_payment
FROM customer as c, appointment as a, payment as p
WHERE c.customer_id = a.customer_id
AND a.appointment_id = p.appointment_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(p.amount + p.tip_amount) = (
    SELECT MAX(total_amount) FROM (
        SELECT SUM(p1.amount + p1.tip_amount) AS total_amount
        FROM appointment as a1, payment as p1
        WHERE a1.appointment_id = p1.appointment_id
        GROUP BY a1.customer_id
    ) AS totals
);
                                
-- SQL Query 10: Create your own non-trivial SQL query 
-- 					-> must use at least three tables in FROM clause  
-- 					-> must use aliasing or renaming at least once 
-- 				throughout SQL query  
-- Goal: Display the most important services of the nail salon.
-- Display: List of the services which bring the most benefit to the nail salon and the total money that they contributed to the business.

SELECT s.service_name, SUM(p.amount + p.tip_amount) AS total_payment
FROM service as s, appointment_service as aps, appointment as a, payment as p
WHERE s.service_id = aps.service_id
AND aps.appointment_id = a.appointment_id
AND a.appointment_id = p.appointment_id
GROUP BY s.service_name
HAVING SUM(p.amount + p.tip_amount) = (
    SELECT MAX(service_total_payment) FROM (
        SELECT SUM(p1.amount + p1.tip_amount) AS service_total_payment
        FROM service as s1, appointment_service as aps1, appointment as a1, payment as p1
        WHERE s1.service_id = aps1.service_id
        AND aps1.appointment_id = a1.appointment_id
        AND p1.appointment_id = a1.appointment_id
        GROUP BY s1.service_name
    ) AS totals
);


-- ************************************ --
--         Additional Queries           --
-- Test constraint for the foreign key  --
-- Using the customer and appointment table     --
-- ************************************ --

-- The 'customer_id' is a FOREIGN KEY in the APPOINTMENT table
-- Refers to the 'customer_id' which is the PRIMARY KEY in the CUSTOMER table
-- Setting: ON DELETE RESTRICT, ON UPDATE CASCADE

-- Insert a new test customer
INSERT INTO CUSTOMER (customer_id, first_name, last_name, phone)
VALUES (999, 'Test', 'User', '000-000-0000');
SELECT * FROM CUSTOMER WHERE customer_id = 999;

-- Insert an appointment for the test customer
INSERT INTO APPOINTMENT (appointment_id, customer_id, staff_id, appointment_date, start_time)
VALUES (999, 999, 1, '2025-08-01', '09:00:00');
SELECT * FROM APPOINTMENT WHERE customer_id = 999;

-- Test ON UPDATE CASCADE by updating the customer's ID
UPDATE CUSTOMER SET customer_id = 998 WHERE customer_id = 999;
SELECT * FROM CUSTOMER WHERE customer_id = 998;
SELECT * FROM APPOINTMENT WHERE customer_id = 998;

-- Test Delete the appointment first, then delete the customer
DELETE FROM APPOINTMENT WHERE appointment_id = 999;
SELECT * FROM APPOINTMENT WHERE customer_id = 998;
DELETE FROM CUSTOMER WHERE customer_id = 998;
SELECT * FROM CUSTOMER WHERE customer_id = 998;

