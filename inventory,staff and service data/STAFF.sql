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
-- Table structure for table `STAFF`
--

CREATE TABLE `STAFF` (
  `staff_id` int NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hire_date` date NOT NULL,
  `position` varchar(50) NOT NULL,
  `commission_rate` decimal(5,2) DEFAULT '0.15',
  `specialty` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
-- Indexes for dumped tables
--

--
-- Indexes for table `STAFF`
--
ALTER TABLE `STAFF`
  ADD PRIMARY KEY (`staff_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `STAFF`
--
ALTER TABLE `STAFF`
  MODIFY `staff_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
