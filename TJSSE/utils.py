from django.core.paginator import Paginator

class ExtendPaginator(Paginator):
  def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
      Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
      self.range_num = range_num

  def page(self, number):
      self.page_num = number
      return super(ExtendPaginator, self).page(number)

  def _page_range_ext(self):
      num_count = 2 * self.range_num + 1
      if self.num_pages <= num_count:
          return range(1, self.num_pages + 1)
      else:
          if self.page_num <= self.range_num:
              return range(1, num_count + 1)
          elif self.page_num + self.range_num >= self.num_pages:
              return range(self.num_pages - num_count + 1, self.num_pages + 1)
          else:
              return range(self.page_num - self.range_num, self.page_num + self.range_num)

  page_range_ext = property(_page_range_ext)
