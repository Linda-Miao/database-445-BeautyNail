-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Jul 18, 2025 at 10:34 PM
-- Server version: 8.0.42
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `beautynailnet`
--

-- --------------------------------------------------------

--
-- Table structure for table `INVENTORY`
--

CREATE TABLE `INVENTORY` (
  `inventory_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `category` varchar(50) NOT NULL,
  `color_name` varchar(50) DEFAULT NULL,
  `quantity_in_stock` int DEFAULT '0',
  `unit_cost` decimal(6,2) NOT NULL,
  `retail_price` decimal(6,2) DEFAULT NULL,
  `reorder_level` int DEFAULT '5',
  `supplier_name` varchar(100) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `INVENTORY`
--
ALTER TABLE `INVENTORY`
  ADD PRIMARY KEY (`inventory_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `INVENTORY`
--
ALTER TABLE `INVENTORY`
  MODIFY `inventory_id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
