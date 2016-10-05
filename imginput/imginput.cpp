#include <Python.h>
#include "imginput.h"
#include "gdalreader.h"
#include "illuminant.h"
#include <string>
#include <vector>
#include <boost/make_shared.hpp>

namespace imginput {

multi_img::ptr ImgInput::execute()
{
	if (config.file.empty()) {
		std::cerr << "No input file specified. Try -H to see available options."
				  << std::endl;
		return multi_img::ptr(new multi_img()); // empty image
	}

	bool roiChanged = false;
	bool bandsCropped = false;

	multi_img::ptr img_ptr;
	// try GDAL first as it is better for some formats OpenCV reads, too (e.g. TIFF)
#ifdef WITH_GDAL
	img_ptr = GdalReader(config).readFile();
#endif

	if (img_ptr && !img_ptr->empty()) {
		// GdalReader was used successfully, applied roiChanges & bandCropping
		roiChanged = true;
		bandsCropped = true;
	} else {
		// GDAL failed, try internal method
		img_ptr = multi_img::ptr(new multi_img(config.file));
	}

	// return empty image if both failed
	if (img_ptr->empty())
		return img_ptr;

	// apply ROI
	if (!roiChanged && !config.roi.empty())
	{
		std::vector<int> roiVals;
		if (!ImgInput::parseROIString(config.roi, roiVals)) {
			// Parsing of ROI String failed
			std::cerr << "Ignoring invalid ROI specification" << std::endl;
		} else {
			applyROI(*img_ptr, roiVals);
		}
	}

	// crop spectrum - maybe we used a fancy file reader that cropped the bands already
	if (!bandsCropped)
		cropSpectrum(*img_ptr);

	// return empty image on failure
	if (img_ptr->empty())
		return img_ptr;

	// normalize L2 magnitudes
	if (config.normalize) {
		img_ptr->normalize_magnitudes();
	}

	// compute gradient
	if (config.gradient) {
		img_ptr->apply_logarithm();
		*img_ptr = img_ptr->spec_gradient();
	}

	// reduce number of bands
	if (config.bands > 0 && config.bands < (int)img_ptr->size()) {
		*img_ptr = img_ptr->spec_rescale(config.bands);
	}

	// alter illumination
	applyIllumination(*img_ptr);

	return img_ptr;
}

multi_img::ptr ImgInput::load(const std::string &filename)
{
	ImgInputConfig cfg;
	cfg.file = filename;
	return ImgInput(cfg).execute();
}

bool ImgInput::parseROIString(const std::string &str, std::vector<int> &vals)
{
	int ctr = 0;
	std::string::size_type prev_pos = 0, pos = 0;
	while ((pos = str.find(':', pos)) != std::string::npos) {
		vals.push_back(atoi(str.substr(prev_pos, pos - prev_pos).c_str()));
		prev_pos = ++pos;
		++ctr;
	}
	vals.push_back(atoi(str.substr(prev_pos, pos - prev_pos).c_str()));
	return ctr == 3;
}

void ImgInput::applyROI(multi_img &img, std::vector<int>& vals)
{
	img = multi_img(img, cv::Rect(vals[0], vals[1], vals[2], vals[3]));
}

void ImgInput::cropSpectrum(multi_img& img)
{
	if ((config.bandlow > 0) ||
		(config.bandhigh > 0 && config.bandhigh < (int)img.size() - 1)) {

		// if bandhigh is not specified, do not limit
		int bandhigh =
		        (config.bandhigh == 0) ? (img.size() - 1) : config.bandhigh;

		// correct input?
		if (config.bandlow > bandhigh || bandhigh > (int)img.size() - 1) {
			std::cerr << "Inconsistent bandlow, bandhigh values specified!"
			          << std::endl;
			img = multi_img();
			return;
		}

        img = multi_img(img, config.bandlow, bandhigh);
	}
}

void ImgInput::applyIllumination(multi_img &img)
{
	if (config.removeIllum > 0) {
		Illuminant il(config.removeIllum);
		// first get normalization right for our range
		il.setNormalization(img.meta[0].center, img.meta[img.size()-1].center);
		img.apply_illuminant(il, true);
	}
	if (config.addIllum > 0) {
		Illuminant il(config.addIllum);
		il.setNormalization(img.meta[0].center, img.meta[img.size()-1].center);
		img.apply_illuminant(il);
	}
}

} //namespace
