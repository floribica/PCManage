-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema genci
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `genci` DEFAULT CHARACTER SET utf8;
USE `genci`;

-- -----------------------------------------------------
-- Table `genci`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`computers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`computers` (
  `serial_nr` VARCHAR(45) NOT NULL,
  `model` VARCHAR(45) NOT NULL,
  `cpu` VARCHAR(45) NULL,
  `ram` VARCHAR(45) NULL,
  `storage_type` VARCHAR(45) NULL,
  `storage_value` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (`serial_nr`),
  UNIQUE INDEX `serial_nr_UNIQUE` (`serial_nr` ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`request` (
  `request_id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `fushata` VARCHAR(45) NOT NULL,
  `request_by` VARCHAR(45) NOT NULL,
  `authorization_date` DATETIME NULL,
  PRIMARY KEY (`request_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`hrs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`hrs` (
  `hr_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  `request_id` INT NOT NULL,
  PRIMARY KEY (`hr_id`),
  INDEX `fk_hrs_request1_idx` (`request_id` ASC),
  CONSTRAINT `fk_hrs_request1`
    FOREIGN KEY (`request_id`)
    REFERENCES `genci`.`request` (`request_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`headsets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`headsets` (
  `headset_id` INT NOT NULL AUTO_INCREMENT,
  `adapter_model` VARCHAR(45) NOT NULL,
  `adapter_sn` VARCHAR(45) NOT NULL,
  `headset_model` VARCHAR(45) NOT NULL,
  `headset_sn` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (`headset_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`others`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`others` (
  `other_id` INT NOT NULL AUTO_INCREMENT,
  `mouse` INT NULL,
  `keyboard` INT NULL,
  `dp_vga` INT NULL,
  `ac` INT NULL,
  `lan` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (`other_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`monitors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`monitors` (
  `monitor_id` INT NOT NULL AUTO_INCREMENT,
  `model` VARCHAR(45) NOT NULL,
  `model_sn` VARCHAR(45) NOT NULL,
  `size` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (`monitor_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`pc_actions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`pc_actions` (
  `pc_action_id` INT NOT NULL AUTO_INCREMENT,
  `returns` INT NOT NULL DEFAULT 0,
  `created_date` DATETIME NOT NULL DEFAULT now(),
  `rikthim_date` DATETIME NOT NULL DEFAULT now() ON UPDATE now(),
  `hr_id` INT NOT NULL,
  `computer_serial_nr` VARCHAR(45) NOT NULL,
  `headset_id` INT NOT NULL,
  `monitor_id` INT NOT NULL,
  `other_id` INT NOT NULL,
  `fushata` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`pc_action_id`),
  INDEX `fk_pc_actions_hrs_idx` (`hr_id` ASC),
  INDEX `fk_pc_actions_computers1_idx` (`computer_serial_nr` ASC),
  INDEX `fk_pc_actions_headsets1_idx` (`headset_id` ASC),
  INDEX `fk_pc_actions_monitors1_idx` (`monitor_id` ASC),
  INDEX `fk_pc_actions_others1_idx` (`other_id` ASC),
  CONSTRAINT `fk_pc_actions_hrs`
    FOREIGN KEY (`hr_id`)
    REFERENCES `genci`.`hrs` (`hr_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pc_actions_computers1`
    FOREIGN KEY (`computer_serial_nr`)
    REFERENCES `genci`.`computers` (`serial_nr`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pc_actions_headsets1`
    FOREIGN KEY (`headset_id`)
    REFERENCES `genci`.`headsets` (`headset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pc_actions_monitors1`
    FOREIGN KEY (`monitor_id`)
    REFERENCES `genci`.`monitors` (`monitor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pc_actions_others1`
    FOREIGN KEY (`other_id`)
    REFERENCES `genci`.`others` (`other_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `genci`.`uploads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `genci`.`uploads` (
  `upload_id` INT NOT NULL AUTO_INCREMENT,
  `file` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `pc_action_id` INT NOT NULL,
  PRIMARY KEY (`upload_id`),
  INDEX `fk_uploads_pc_actions1_idx` (`pc_action_id` ASC),
  CONSTRAINT `fk_uploads_pc_actions1`
    FOREIGN KEY (`pc_action_id`)
    REFERENCES `genci`.`pc_actions` (`pc_action_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Final SQL settings reset
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

